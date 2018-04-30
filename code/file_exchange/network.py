#!/usr/bin/env python3

from enum import Enum
import gevent
import random
import sys


def emulate_transfer(header, m, net, conf):
    '''
    Attempts to send m to a node in header.
    Emulates traffic by sleeping ((m.size+header_size)/bandwidth).


    header: list of potential peers addresses
    m: the message, a network.Message object
    net: the Network object, to retrieve Device from address
    conf: configuration variables (bandwidth and header_size)

    Returns True if m was sent, False otherwise'''

    if conf['send_strategy'] == 'random':
        # 1 - Try to send to a random device: we always sleep
        # Fail if device is offline, else send to dst
        gevent.sleep((m.size+conf['header_size'])/conf['bandwidth'])
        dst = net.get_device(random.choice(header))
        if dst.is_online():
            dst.receive(m)
            return True
        return False

    elif conf['send_strategy'] == 'random_connected':
        # 2 - Ping devices to find a random *connected* one.
        # Fail if no connected device, else send pick device.
        devices = [net.get_device(addr) for addr in header]
        gevent.sleep(conf['ping_time'])
        connected_devices = [d for d in devices if d.is_online()]

        if len(connected_devices) == 0:
            return False

        gevent.sleep((m.size+conf['header_size'])/conf['bandwidth'])
        random.choice(connected_devices).receive(m)
        return True
    else:
        raise ValueError("conf['send_strategy'] is not valid.")


class MessType(Enum):
    CHUNK = 1
    ACK = 2


MAX_MESSAGE_ID = 2**63


class Message:
    def __init__(self, header, typ, file_id, chunk_id, size, m_id=None):
        if m_id is None:
            self.id = random.randint(0, MAX_MESSAGE_ID)
        else:
            self.id = m_id
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
