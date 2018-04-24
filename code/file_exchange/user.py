#!/usr/bin/env python3

from . import model, device, config, file, utils
import numpy as np
import gevent

FILE_ID_SIZE = 10


class User(gevent.Greenlet):
    def __init__(self, global_view, net, conf=config.default):
        gevent.Greenlet.__init__(self)
        self.model = model.get_random()

        # Create devices
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
        self.name = utils.random_name()

        self.receiving_files = {}

        self.state_history, self.devices_history = self.model.sample(
            length=conf['n_rounds'])

    # Overriding Greenlet
    def _run(self):
        self.loop()

    def loop(self):
        while True:
            # Initial round
            if self.current_round is None:
                self.current_round = 0
            # Break if all rounds done
            elif self.current_round == self.conf['n_rounds'] - 1:
                print("Returned")
                return
            # Else increment round
            else:
                self.current_round += 1

            # Update devices' state
            for d_id, is_online in \
                    enumerate(self.devices_history[self.current_round]):
                self.devices[d_id].update_state(is_online)

            # Sleep until next round
            gevent.sleep(self.conf['period'].total_seconds())

    def init_file_receive(self, remote_device):
        d = self.get_online_device()

        H_rdv = d.build_route("receiver")
        file_id = utils.random_string(FILE_ID_SIZE)

        self.receiving_files[file_id] = file.File(
            self.conf['n_chunks'], file_id)

        # This exchange is out of band
        remote_device.init_file_send(H_rdv, file_id)

    def receive_chunk(self, m):
        self.receiving_files[m.file_id].ack(m.chunk_id)

        if self.receiving_files[m.file_id].all_shared():
            # Maybe do something else
            del self.receiving_files[m.file_id]

    def has_online_devices(self):
        return self.devices_history[self.current_round].sum() != 0

    def get_online_device(self):
        return self.devices[
            np.random.choice(
                np.where(
                    self.devices_history[self.current_round]
                )[0]
            )
        ]

    def get_prediction(self, device_id):
        return self.model.predict(
            1, device_id, self.state_history[self.current_round])[0]

    # Overriding Greenlet
    def __str__(self):
        return "User({})".format(self.name)
