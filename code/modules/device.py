#!/usr/bin/env python3

from . import config, peers_view, file, network
from .utils import random_string, hash_layer
from datetime import timedelta, datetime
import numpy as np
import pandas as pd
import random

ADDR_SIZE = 12


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

        # File-exchange related
        self.sending_files = {}
        self.sending_files_routes = {}

        # maps hash of route's layer -> previously picked device from layer
        self.connected_to = {}

    def register_to_global_view(self, is_online):
        self.is_online = is_online
        if self.is_online:
            self.global_view.put(
                datetime.now(),
                self.addr,
                self.type,
                self.owner.get_prediction(self.device_id)
            )

    def act(self):
        if not self.is_online:
            return

        self.random_peer_sampling()

        # TODO: bandwidth
        for f in self.sending_files:
            self.send_file_chunk(f)

    def init_file_send(self, H_rdv, file_id):
        f = file.File(self.conf['n_chunks'])

        self.sending_files[f.id] = f

        route = [None] * self.conf['n_layers']
        route[:self.conf['n_layers'] // 2] = self.build_route("sender")
        route[self.conf['n_layers'] // 2:] = H_rdv

        self.sending_files_routes[f.id] = route

    def send_file_chunk(self, f):
        if f.all_shared():
            print("[Device.send_file_chunk] file {} already completed".format(
                f.id))
            self.complete_file_exchange()
            return

        self.send(None, self.sending_files_routes[f.id],
                  network.Message(
                      typ=network.MessType.CHUNK,
                      file_id=f.id,
                      chunk_id=f.select_chunk()
        ))

    def send(self, src, route, m):
        if not self.is_online:
            return

        # Am I the receiver?
        if m.type == network.MessType.CHUNK and \
                m.file_id in self.owner.receiving_files:
            self.owner.receive_chunk(m)
            # Forward ACK back to source

        # because layers are encrypted, we are not supposed to be able
        # to read more than the first one (layers are rotated at ever hop)
        layer = route[0]
        h = hash_layer(layer)
        # Firt connection on this route: pick a device in layer
        if not h in self.connected_to:
            self.connected_to[h] = random.choice(layer['addr'])

        d = self.net.get_device(self.connected_to[h])
        # If the device we were already connected with is offline
        if not d.is_online:
            # Try to find another online device and exit
            others = layer[layer['addr'] != d.addr]['addr']
            others = [
                addr for addr in others if self.net.get_device(addr).is_online]
            # We found an online device, connect to it
            if len(others) > 0:
                self.connected_to[h] = random.choice(others)

            return

        # Rotate layers so that next device sees the right layer in route[0]
        route.append(route[0])
        del route[0]
        # And send
        d.send(self, route, m)
        return

    def complete_file_exchange(self, f):
        if f.id in self.sending_files and f.all_shared():
            del self.sending_files[f.id]
            del self.sending_files_routes[f.id]

    def random_peer_sampling(self):
        self.peers_view.insert(
            self.global_view.get_sample(
                n=self.gossip_size,
                exclude_addr=self.addr))
        # if len(self.peers_view.view) == 0:
        #     print("Device's RPS returned 0 devices!"
        #           " Global peers view has {}.".format(
        #         len(self.global_view.view)))
        #     expiration_limit = datetime.now() - self.conf['period']
        #     print("Expiration time:", expiration_limit)
        #     print(self.global_view.view)

    def build_route(self, role):
        if role == "receiver":
            # 2 layers planned in advance
            n_layers = self.conf['n_layers'] // 2 + 1
        elif role == "sender":
            n_layers = self.conf['n_layers'] // 2
        else:
            raise ValueError("role should be either 'sender' or 'receiver'")

        route = [pd.DataFrame() for _ in range(n_layers)]
        view = self.peers_view.view.copy()

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

            # Converged when all layers are converged
            if not converged:
                converged = all(converged_layers)

        return route
