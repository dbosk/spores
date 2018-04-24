#!/usr/bin/env python3


class Network:
    def __init__(self):
        self.devices = dict()

    def add_device(self, d):
        self.devices[d.addr] = d

    def get_device(self, addr):
        d = self.devices.get(addr)
        if d is None:
            raise ValueError("{} is not in the nlist of devices.".format(addr))
        return d
