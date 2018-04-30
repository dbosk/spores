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
        if self.is_online:
            self.global_view.put(
                datetime.now(),
                self.addr,
                self.type,
                self.owner.get_prediction(self.device_id)
            )

    def rps(self):
        if self.is_online:
            self.random_peer_sampling()

    def random_peer_sampling(self):
        self.peers_view.insert(
            self.global_view.get_sample(
                n=self.gossip_size,
                exclude_addr=self.addr))
        # if len(self.peers_view.view) == 0:
        #     print("Device's RPS returned 0 devices! Global peers view has {}.".format(
        #         len(self.global_view.view)))
        #     expiration_limit = datetime.now() - self.conf['period']
        #     print("Expiration time:", expiration_limit)
        #     print(self.global_view.view)

    def build_random_route(self, nodes_per_layer):
        n_layers = len(nodes_per_layer)
        route = [pd.DataFrame() for _ in range(n_layers)]
        view = self.peers_view.view.copy()

        for l_id in range(n_layers):
            while len(route[l_id]) < nodes_per_layer[l_id]:
                if len(view) == 0:
                    raise Exception("Damn, son")
                # Pick a device from view without replacement
                d = view.iloc[np.random.choice(len(view))]
                route[l_id] = route[l_id].append(d)
                view.drop(d.name, inplace=True)

        return route

    def build_route(self, role):
        if role == "receiver":
            # 2 layers planned in advance
            n_layers = self.conf['n_layers'] // 2 + 1
        elif role == "sender":
            n_layers = self.conf['n_layers'] // 2
        else:
            raise ValueError("role should be either 'sender' or 'receiver'")

        # print("[build route] Creating '{}' route with {} layers".format(
        #     role, n_layers))

        route = [pd.DataFrame() for _ in range(n_layers)]
        view = self.peers_view.view.copy()

        if len(view) == 0:
            raise("Dayum")

        converged = False
        while not converged:
            converged_layers = [False for _ in range(n_layers)]
            # Iteratively add one device per layer until converged
            for l_id in range(n_layers):
                if len(route[l_id]) > 0:
                    # Probability that all devices of layer will be offline
                    p_failure = (1 - route[l_id]['p']).prod()
                    # layer is converged when p_failure is below threshold
                    converged_layers[l_id] = \
                        p_failure < self.conf['layer_threshold']

                    # print("[build route] Layer {} has p_fail={} => {}".format(
                    #     l_id, p_failure,
                    #     "converged" if converged_layers[l_id]
                    #     else "not converged"))

                    # Skip this layer if converged
                    if converged_layers[l_id]:
                        continue

                # Else add a node to layer

                # If view is empty, break
                if len(view) == 0:
                    print("[build route] No more available nodes: "
                          "early abort.")
                    converged = True
                    break

                # Pick a device from view without replacement
                d = view.iloc[np.random.choice(len(view))]
                route[l_id] = route[l_id].append(d)
                view.drop(d.name, inplace=True)
                # print("[build route] Added device with p={:.2f} to layer {}. "
                #       "View has size {}. p_failure={:.5f}".format(
                #           d['p'], l_id, len(view),
                #           (1 - route[l_id]['p']).prod()))

            # Converged when all layers are converged
            if not converged:
                converged = all(converged_layers)

        # if len(view) == 0:
        #     print("[build_route] view size={} gossip_size={}".format(
        #         len(self.peers_view.view), self.gossip_size))
        #     print("[build_route] number of online devices={}".format(
        #         sum([d.is_online for d in self.net.devices.values()])))
        #     print(route)

        return route

    def receive_message(self, message):
        return


def random_string(n):
    return ''.join(
        [random.choice(string.ascii_lowercase+string.digits)
         for _ in range(n)])
