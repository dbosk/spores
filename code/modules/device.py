#!/usr/bin/env python3

from . import config, peers_view
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
            conf=config.default):

        self.addr = random_string(ADDR_SIZE)
        self.conf = conf
        self.device_id = device_id
        self.global_view = global_view
        self.gossip_size = conf['gossip_size']
        self.is_online = False
        self.net = net
        self.owner = owner
        self.peers_view = peers_view.PeersView(conf)
        self.type = device_type

        net.add_device(self)

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

    def build_route(self, role):
        if role == "receiver":
            # 2 layers planned in advance
            n_layers = self.conf['n_layers'] // 2 + 1
        elif role == "sender":
            n_layers = self.conf['n_layers'] // 2
        else:
            raise ValueError("role should be either 'sender' or 'receiver'")

        route = []
        view = self.peers_view.view.copy()
        for _ in range(n_layers):
            layer, view = self.build_layer(view)
            route.append(layer)

        return route

    def build_layer(self, view=None):
        if view is None:
            view = self.peers_view.view.copy()

        print("[build_layer] Starting with view of size {} "
              "and layer_threshold of {}.".format(
                  view.shape[0], self.conf['layer_threshold']))

        layer = pd.DataFrame()
        p = 1
        i = 0
        while p > self.conf['layer_threshold']:
            if len(view) == 0:
                print("[build_layer it. {}] "
                      "No more devices in view: early abort.".format(i))
                break
            # Pick a device from view without replacement
            d = view.iloc[np.random.choice(len(view))]
            layer = layer.append(d)
            view.drop(d.name, inplace=True)
            p *= (1 - d['p'])

            print("[build_layer it. {}] "
                  "Selected device having proba of {:.2f}. "
                  "Now view has size {} and p={:.4f}".format(
                      i, d['p'], view.shape[0], p))
            i += 1
        print()

        return layer, view

    def receive_message(self, message):
        return


def random_string(n):
    return ''.join(
        [random.choice(string.ascii_lowercase+string.digits)
         for _ in range(n)])
