#!/usr/bin/env python3

from enum import Enum
import gevent


def emulate_transfer(dst, m, header_size, bandwidth):
    '''
    Sleeps the duration of the file transfer ((m.size+header_size)/bandwidth),
    Drops the packet if dst is offline, else send it to dst.

    dst: device.Device object
    m: network.Message object
    header_size: size of the header
    bandwidth: numeric value in MB/s

    Returns True if m was sent, False otherwise'''

    gevent.sleep((m.size+header_size)/bandwidth)

    if dst.is_online():
        dst.receive(m)
        return True

    return False


class MessType(Enum):
    CHUNK = 1
    ACK = 2


class Message:
    def __init__(self, header, typ, file_id, chunk_id, size):
        self.header = header
        self.type = typ
        self.file_id = file_id
        self.chunk_id = chunk_id
        self.size = size


class Network:
    def __init__(self):
        self.devices = dict()
        self.lock = gevent.lock.Semaphore()

    def add_device(self, d):
        self.lock.acquire()
        self.devices[d.addr] = d
        self.lock.release()

    def get_device(self, addr):
        self.lock.acquire()
        d = self.devices.get(addr)
        self.lock.release()
        if d is None:
            raise ValueError("{} is not in the list of devices.".format(addr))
        return d
