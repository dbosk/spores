#!/usr/bin/env python3

import numpy as np
from . import model, device, config


class User:
    def __init__(self, global_view, net, conf=config.default):
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

        self.state_history, self.devices_history = self.model.sample(
            length=conf['n_rounds'])

    def act(self):
        if self.current_round is None:
            self.current_round = 0
        else:
            self.current_round += 1

        for d_id, is_online in \
                enumerate(self.devices_history[self.current_round]):
            self.devices[d_id].act(is_online)

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
