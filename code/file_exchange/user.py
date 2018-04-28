#!/usr/bin/env python3

from . import model, device, config, file, utils, monitor
import gevent
import random
import time

MONITOR_COLUMNS = ['t', 'experiment_id', 'user', 'current_round']


class User(gevent.Greenlet):
    def __init__(self, global_view, net, conf=config.default):
        gevent.Greenlet.__init__(self)

        self.name = utils.random_name()

        # Create model and devices
        self.model = model.get_random()
        self.n_devices = self.model.n_obs
        self.devices = [None] * self.n_devices
        self.devices_addr = [None] * self.n_devices

        for d_id in range(self.n_devices):
            self.devices[d_id] = device.Device(
                self, global_view, net, d_id,
                self.model.devices_type[d_id], conf)
            self.devices_addr[d_id] = self.devices[d_id].addr

        self.conf = conf
        self.current_round = None
        self.death_requested = False
        self.monitor = monitor.Monitor(
            MONITOR_COLUMNS,
            conf['output_dir'],
            "user_"+self.name,
            conf['do_monitor'])

        # Any user's device can receive chunks
        self.receiving_files = {}
        # Any user's device can receive ACK, but only source can send chunks
        self.sending_files = {}
        self.lock = gevent.lock.Semaphore()

        self.state_history, self.devices_history = self.model.sample(
            length=conf['n_rounds'])

    # Overriding Greenlet
    def _run(self):
        # Starting devices greenlets
        for d in self.devices:
            d.start()

        while (not self.death_requested) and \
            (self.current_round is None or
             self.current_round < self.conf['n_rounds'] - 1):
            t_start = time.perf_counter()
            self.update_state()

            # Sleep until next round

            gevent.sleep(self.conf['period'].total_seconds() -
                         (time.perf_counter() - t_start))

            # print("User {}: round #{}/{} in {:.2f}s (die={})".format(
            #     self.name, self.current_round+1,
            #     self.conf['n_rounds'], time.perf_counter() - t_start,
            #     self.death_requested))

        self.monitor.save()

        for d in self.devices:
            d.please_die()

        gevent.joinall(self.devices)
        print("User {} is done.".format(self.name))

    def please_die(self):
        self.death_requested = True

    def update_state(self):
        self.lock.acquire()
        # Initial round
        if self.current_round is None:
            self.current_round = 0
        # Else increment round
        elif self.current_round < self.conf['n_rounds'] - 1:
            self.current_round += 1
        else:
            self.lock.release()
            return

        self.monitor.put([
            time.perf_counter(),
            self.conf['experiment_id'],
            self.name,
            self.current_round
        ])

        # Update devices' state
        for d_id, is_online in \
                enumerate(self.devices_history[self.current_round]):

            self.devices[d_id].update_state(
                is_online,
                self.get_prediction(d_id))
        self.lock.release()

    #### File sharing ###
    def init_file_receive(self, remote_user):
        self.lock.acquire()

        if self.current_round is None:
            self.lock.release()
            raise Exception(
                "User {} must do a first round before exchanging files".format(
                    self.name))

        d = self.get_online_device()
        if d is None:
            self.lock.release()
            raise Exception("No online devices")

        f = file.File(self.conf)

        # route = L_RV + L_k + ... + L_l
        try:
            route = d.build_route("receiver")
        except:
            self.lock.release()
            raise
        # H_rdv_forward = (L_RV + L_k + ... + L_l) + L_B (my devices)
        H_rdv_forward = route + [self.get_all_devices_addr()]
        # H_rdv_backward = (L_l + ... + L_k + L_RV)
        H_rdv_backward = route[::-1]

        # This exchange is out of band
        # But can fail, in which case we cancel the file exchange
        try:
            forward_route, backward_route = remote_user.init_file_send(
                H_rdv_forward, H_rdv_backward, f.copy())
        except:
            self.lock.release()
            raise

        self.receiving_files[f.id] = {
            'f': f,
            'forward_route': forward_route,
            'backward_route': backward_route,
        }

        self.lock.release()

        return self.receiving_files[f.id]

    def init_file_send(self, H_rdv_forward, H_rdv_backward, f):
        self.lock.acquire()
        if self.current_round is None:
            self.lock.release()
            raise Exception(
                "User {} must do a first round before exchanging files".format(
                    self.name))

        d = self.get_online_device()
        if d is None:
            self.lock.release()
            raise Exception("No online devices")

        try:
            file_info = d.init_file_send(H_rdv_forward, H_rdv_backward, f)
        except:
            self.lock.release()
            raise
        self.sending_files[f.id] = file_info
        self.lock.release()

        return file_info['forward_route'], file_info['backward_route']

    ### Getters ###
    def get_all_devices_addr(self):
        return [d.addr for d in self.devices]

    def get_prediction(self, device_id):
        return self.model.predict(
            1, device_id, self.state_history[self.current_round])[0]

    def get_online_device(self):
        online_devices = [d for d in self.devices if d.is_online()]
        if len(online_devices) == 0:
            return None
        return random.choice(online_devices)

    # Overriding Greenlet
    def __str__(self):
        return "User({})".format(self.name)
