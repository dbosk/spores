#!/usr/bin/env python3

import numpy as np
from .peers_view import PeersView

ADDR_SIZE = 12

DEFAULT_GOSSIP_SIZE = 6
DEFAULT_VIEW_SIZE = 20


class Device:
    def __init__(
            self, owner, global_view,
            gossip_size=DEFAULT_GOSSIP_SIZE,
            view_size=DEFAULT_VIEW_SIZE):

        self.owner = owner
        self.global_view = global_view
        self.gossip_size = gossip_size
        self.view_size = view_size
        self.peers_view = PeersView(view_size)
        self.addr = random_string(ADDR_SIZE)

        self.files = []  # ?

    def random_peer_sampling(self):
        self.peers_view.insert(
            self.global_view.get_sample(n=self.gossip_size))


def random_string(n):
    ''.join(
        [random.choice(string.ascii_lowercase+string.digits)
         for _ in range(n)])
