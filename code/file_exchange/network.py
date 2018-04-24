#!/usr/bin/env python3

from enum import Enum


class MessType(Enum):
    CHUNK = 1
    ACK = 2


class Message:
    def __init__(self, typ, file_id, chunk_id):
        self.type = typ
        self.file_id = file_id
        self.chunk_id = chunk_id


class Network:
    def __init__(self):
        self.devices = dict()

    def add_device(self, d):
        self.devices[d.addr] = d

    def get_device(self, addr):
        d = self.devices.get(addr)
        if d is None:
            raise ValueError("{} is not in the list of devices.".format(addr))
        return d
