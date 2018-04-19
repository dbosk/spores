#!/usr/bin/env python3

import numpy as np
from . import model, device


class User:
    def __init__(self, global_view, net,
                 gossip_size=device.DEFAULT_GOSSIP_SIZE):
        self.model = model.get_random()

        self.n_devices = self.model.n_obs
        # Create devices
        self.devices = [None] * self.n_devices
        self.devices_addr = [None] * self.n_devices
        for d_id in range(self.n_devices):
            self.devices[d_id] = device.Device(
                self, global_view, net, d_id,
                self.model.devices_type[d_id], gossip_size)
            self.devices_addr[d_id] = self.devices[d_id].addr

        self.current_state = None
        self.state_history = []
        self.devices_history = []

    def act(self):
        states, devices = self.model.sample(
            length=1, previous_state=self.current_state)
        # Model.sample returns array indexed by time
        # here we need sample[0] = t+1
        self.current_state = states[0]
        self.state_history.append(self.current_state)
        devices_state = devices[0]
        self.devices_history.append(devices_state)

        for d_id, is_online in enumerate(devices_state):
            self.devices[d_id].act(is_online)

    def plan_file_exchange(self, route):

    def has_online_devices(self):
        return self.devices_history[-1].sum() != 0

    def get_online_device(self):
        return self.devices[np.random.choice(
            np.where(self.devices_history[-1])[0])]

    def get_prediction(self, device_id):
        return self.model.predict(1, device_id, self.current_state)[0]
