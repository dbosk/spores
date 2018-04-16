#!/usr/bin/env python3

import numpy as np
from . import model, device


class User:
    def __init__(self, global_view):
        self.model = model.get_random()

        self.n_devices = self.model.n_obs
        # Create devices
        self.devices = [None] * self.n_devices
        for d_id in range(self.n_devices):
            self.devices[d_id] = device.Device(self, global_view, d_id)

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
        self.devices_history.append(devices[0])

        for d_id, is_online in enumerate(devices[0]):
            self.devices[d_id].act(is_online)

    def get_prediction(self, device_id):
        return self.model.predict(1, device_id, self.current_state)[0]
