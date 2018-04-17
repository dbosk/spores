#!/usr/bin/env python3

# import numpy as np
from .peers_view import PeersView
from datetime import timedelta, datetime
import random
import string

ADDR_SIZE = 12

DEFAULT_GOSSIP_SIZE = 10
DEFAULT_EXPIRATION_PERIOD = timedelta(seconds=1)


class Device:
    def __init__(
            self, owner, global_view, device_id,
            gossip_size=DEFAULT_GOSSIP_SIZE,
            expiration_period=DEFAULT_EXPIRATION_PERIOD):

        self.owner = owner
        self.global_view = global_view
        self.device_id = device_id
        self.gossip_size = gossip_size
        self.peers_view = PeersView(expiration_period)
        self.addr = random_string(ADDR_SIZE)
        self.is_online = False

        self.files = []  # ?

    def act(self, is_online):
        self.is_online = is_online
        if is_online:
            self.global_view.put(
                datetime.now(),
                self.addr,
                self.owner.get_prediction(self.device_id)
            )
            self.random_peer_sampling()

    def random_peer_sampling(self):
        self.peers_view.insert(
            self.global_view.get_sample(
                n=self.gossip_size,
                exclude_addr=self.addr))


def random_string(n):
    return ''.join(
        [random.choice(string.ascii_lowercase+string.digits)
         for _ in range(n)])
