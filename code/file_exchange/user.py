#!/usr/bin/env python3

from . import model, device, config, file, utils
import gevent
import random


class User(gevent.Greenlet):
    def __init__(self, global_view, net, conf=config.default):
        gevent.Greenlet.__init__(self)
        self.model = model.get_random()

        # Create devices
        self.n_devices = self.model.n_obs
        self.devices = [None] * self.n_devices
        self.devices_addr = [None] * self.n_devices
        #self.devices_threads = gevent.pool.Group()
        for d_id in range(self.n_devices):
            self.devices[d_id] = device.Device(
                self, global_view, net, d_id,
                self.model.devices_type[d_id], conf)
            self.devices_addr[d_id] = self.devices[d_id].addr
            self.devices[d_id].start()
            # self.devices_threads.start(self.devices[d_id])

        self.conf = conf
        self.current_round = None
        self.name = utils.random_name()

        # Any user's device can receive chunks
        self.receiving_files = {}
        # Any user's device can receive ACK, but only source can send chunks
        self.sending_files = {}
        self.lock = gevent.lock.Semaphore()

        self.state_history, self.devices_history = self.model.sample(
            length=conf['n_rounds'])

    # Overriding Greenlet
    def _run(self):
        while self.current_round is None or \
                self.current_round < self.conf['n_rounds'] - 1:
            self.update_state()

            # Sleep until next round
            gevent.sleep(self.conf['period'].total_seconds())

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
            raise Exception("User must do a first ")
        d = self.get_online_device()

        f = file.File(self.conf['file_size'], self.conf['chunk_max_size'])

        # route = L_RV + L_k + ... + L_l
        route = d.build_route("receiver")
        # H_rdv_forward = (L_RV + L_k + ... + L_l) + L_B (my devices)
        H_rdv_forward = route + [self.get_all_devices_addr()]
        # H_rdv_backward = (L_l + ... + L_k + L_RV)
        H_rdv_backward = route[::-1]

        # This exchange is out of band
        forward_route, backward_route = remote_user.init_file_send(
            H_rdv_forward, H_rdv_backward, f.copy())

        self.receiving_files[f.id] = {
            'file': f,
            'forward_route': forward_route,
            'backward_route': backward_route,
        }

        self.lock.release()

        return self.receiving_files[f.id]

    def init_file_send(self, H_rdv_forward, H_rdv_backward, f):
        self.lock.acquire()
        d = self.get_online_device()

        file_info = d.init_file_send(H_rdv_forward, H_rdv_backward, f)
        file_info['source_device'] = d
        self.sending_files[f.id] = file_info
        self.lock.release()

        return file_info['forward_route'], file_info['backward_route']

    # def receive_chunk(self, m):
    #     self.receiving_files[m.file_id].ack(m.chunk_id)

    #     if self.receiving_files[m.file_id].all_shared():
    #         # Maybe do something else
    #         del self.receiving_files[m.file_id]

    ### Getters ###
    def get_all_devices_addr(self):
        return [d.addr for d in self.devices]

    def get_prediction(self, device_id):
        return self.model.predict(
            1, device_id, self.state_history[self.current_round])[0]

    def get_online_device(self):
        return random.choice([d for d in self.devices if d.is_online()])

    # Overriding Greenlet
    def __str__(self):
        return "User({})".format(self.name)

    # def has_online_devices(self):
    #     return self.devices_history[self.current_round].sum() != 0
