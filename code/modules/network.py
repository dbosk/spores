#!/usr/bin/env python3


class Network:
    def __init__(self):
        self.devices = dict()

    def add_device(self, d):
        self.devices[d.addr] = d

    def get_device(self, addr):
        d = self.devices.get(addr)
        if d is None or not d.is_online:
            return None
        return d
