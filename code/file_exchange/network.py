#!/usr/bin/env python3

from enum import Enum
import gevent
import random


def emulate_transfer(header, m, net, conf):
    '''
    Sleeps the duration of the file transfer ((m.size+header_size)/bandwidth),
    Then sends the message m to a connected peer in header or fails.

    header: list of potential peers addresses
    m: the message, a network.Message object
    net: the Network object, to retrieve Device from address
    conf: configuration variables (bandwidth and header_size)

    Returns True if m was sent, False otherwise'''

    gevent.sleep((m.size+conf['header_size'])/conf['bandwidth'])

    if conf['send_strategy'] == 'random':
        # 1 - Pick a random device; send if online, fail if offline
        dst = net.get_device(random.choice(header))
        if dst.is_online():
            dst.receive(m)
            return True
        return False

    elif conf['send_strategy'] == 'random_connected':
        # 2 - Pick a random *connected* device and send;
        # Fails if no connected device
        devices = [net.get_device(addr) for addr in header]
        connected_devices = [d for d in devices if d.is_online()]
        if len(connected_devices) == 0:
            return False
        random.choice(connected_devices).receive(m)
        return True
    else:
        raise ValueError("conf['send_strategy'] is not valid.")


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
