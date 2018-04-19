#!/usr/bin/env python3

from .peers_view import PeersView
from datetime import timedelta, datetime
import numpy as np
import pandas as pd
import random
import string

ADDR_SIZE = 12

DEFAULT_GOSSIP_SIZE = 10
DEFAULT_EXPIRATION_PERIOD = timedelta(seconds=1)
MINIMUM_LAYER_PROBA = 1


class Device:
    def __init__(
            self, owner, global_view, net, device_id, device_type,
            gossip_size=DEFAULT_GOSSIP_SIZE,
            expiration_period=DEFAULT_EXPIRATION_PERIOD):

        self.addr = random_string(ADDR_SIZE)
        self.device_id = device_id
        self.global_view = global_view
        self.gossip_size = gossip_size
        self.is_online = False
        self.net = net
        self.owner = owner
        self.peers_view = PeersView(expiration_period)
        self.type = device_type

        net.add_device(self)

        self.files = []  # ?

    def act(self, is_online):
        self.is_online = is_online
        if is_online:
            self.global_view.put(
                datetime.now(),
                self.addr,
                self.type,
                self.owner.get_prediction(self.device_id)
            )
            self.random_peer_sampling()

    def random_peer_sampling(self):
        self.peers_view.insert(
            self.global_view.get_sample(
                n=self.gossip_size,
                exclude_addr=self.addr))

    def plan_route(self, role):
        if role == "receiver":
            # 2 layers planned in advance
            route = []
            route.append(self.pick_devices())
            route.append(self.pick_devices())

        elif role == "sender":

        else:
            raise ValueError("role should be either 'sender' or 'receiver'")

    def pick_devices(self):
        view = self.peers_view.view.copy()

        layer = pd.DataFrame()
        p = 0
        while p < MINIMUM_LAYER_PROBA:
            # Pick a device from view without replacement
            d = view.iloc[np.random.choice(len(view))]
            layer = layer.append(d)
            view.drop(d.name, inplace=True)
            p += d['p']

        return layer


def random_string(n):
    return ''.join(
        [random.choice(string.ascii_lowercase+string.digits)
         for _ in range(n)])
