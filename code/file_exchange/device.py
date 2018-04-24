#!/usr/bin/env python3

from . import config, peers_view, file, network
from .utils import random_string, hash_layer
from datetime import timedelta, datetime
from gevent.queue import Queue
import gevent
import numpy as np
import pandas as pd
import random

ADDR_SIZE = 12


class Device(gevent.Greenlet):
    def __init__(
            self, owner, global_view, net, device_id, device_type,
            conf=config.default):
        gevent.Greenlet.__init__(self)
        self.addr = random_string(ADDR_SIZE)
        self.conf = conf
        self.device_id = device_id
        self.global_view = global_view
        self.gossip_size = conf['gossip_size']
        self.lock = gevent.lock.Semaphore()
        self.net = net
        self.online = gevent.event.Event()
        self.owner = owner
        self.peers_view = peers_view.PeersView(conf)
        self.message_queue = Queue()
        self.type = device_type

        net.add_device(self)

        # Contains only files that this particular device is sending
        self.sending_files = {}

        # maps hash of route's layer -> previously picked device from layer
        self.connected_to = {}

    # Overriding Greenlet
    def _run(self):
        while True:
            self.online.wait()

            # sending_files is going to need locks...
            for f_id, file_info in self.sending_files.items():
                if file_info['f'].all_acknowledged():
                    del self.sending_files[f_id]
                self.send_file_chunk(file_info)

                if not self.is_online():
                    continue

            # TODO: Add locks!
            for m in self.message_queue:
                if m.file_id in self.owner.receiving_files:
                    file_info = self.owner.receiving_files[m.file_id]

                    if m.type != network.MessType.CHUNK:
                        print("dafuq?")

                    file_info['f'].shared(m.chunk_id)

                    self.send_file_ack(file_info, m.chunk_id)

                elif m.file_id in self.owner.sending_files:
                    file_info = self.owner.sending_files[m.file_id]

                    if m.type != network.MessType.ACK:
                        print("dafuq?")

                    file_info['f'].acknowledged(m.chunk_id)

                    if file_info['f'].all_acknowledged():
                        del self.owner.sending_files[m.file_id]

                else:
                    self.forward_message(m)

                # So I should put these everywhere
                # Fits at the end of the for, though, otherwise m would be lost
                if not self.is_online():
                    continue

        return

    # Called from the user's greenlet
    def update_state(self, is_online, p):
        # Set Event according to is_online
        if is_online:
            self.online.set()
        else:
            self.online.clear()
        if self.is_online():
            # If online, register to global view
            self.global_view.put(
                datetime.now(),
                self.addr,
                self.type,
                p
            )

    def init_file_send(self, H_rdv_forward, H_rdv_backward, f):
        # route = L_i + ... + L_j
        route = self.build_route("sender")
        # forward_route = (L_i + ... + L_j) + (L_RV + L_k + ... + L_l + L_B)
        forward_route = route + H_rdv_forward
        # backward_route = (L_l + ... + L_k + L_RV) + (L_j + ... + L_i) + L_A
        backward_route = H_rdv_backward + \
            route[::-1] + [self.owner.get_all_devices_addr()]

        self.sending_files[f.id] = {
            'file': f,
            'forward_route': forward_route,
            'backward_route': backward_route,
        }

        return self.sending_files[f.id]

    ### Messages exchange ###
    def receive(self, message):
        self.message_queue.put(message)

    # def send_file_chunk(self, f):
    #     if f.all_shared():
    #         print("[Device.send_file_chunk] file {} already completed".format(
    #             f.id))
    #         self.complete_file_exchange()
    #         return

    #     self.send(None, self.sending_files_routes[f.id],
    #               network.Message(
    #                   typ=network.MessType.CHUNK,
    #                   file_id=f.id,
    #                   chunk_id=f.select_chunk()
    #     ))

    # def send(self, src, route, m):
    #     if not self.is_online():
    #         return

    #     # Am I the receiver?
    #     if m.type == network.MessType.CHUNK and \
    #             m.file_id in self.owner.receiving_files:
    #         self.owner.receive_chunk(m)
    #         # Forward ACK back to source

    #     # because layers are encrypted, we are not supposed to be able
    #     # to read more than the first one (layers are rotated at ever hop)
    #     layer = route[0]
    #     h = hash_layer(layer)
    #     # Firt connection on this route: pick a device in layer
    #     if not h in self.connected_to:
    #         self.connected_to[h] = random.choice(layer['addr'])

    #     d = self.net.get_device(self.connected_to[h])
    #     # If the device we were already connected with is offline
    #     if not d.is_online():
    #         # Try to find another online device and exit
    #         others = layer[layer['addr'] != d.addr]['addr']
    #         others = [addr for addr in others
    #                   if self.net.get_device(addr).is_online()]
    #         # We found an online device, connect to it
    #         if len(others) > 0:
    #             self.connected_to[h] = random.choice(others)

    #         return

    #     # Rotate layers so that next device sees the right layer in route[0]
    #     route.append(route[0])
    #     del route[0]
    #     # And send
    #     d.send(self, route, m)
    #     return

    # def complete_file_exchange(self, f):
    #     if f.id in self.sending_files and f.all_shared():
    #         del self.sending_files[f.id]
    #         del self.sending_files_routes[f.id]

    # a priori no need lock (only place we use peers_view)
    def build_route(self, role):
        if role == "receiver":
            # 2 layers planned in advance
            n_layers = self.conf['n_layers'] // 2 + 1
        elif role == "sender":
            n_layers = self.conf['n_layers'] // 2
        else:
            raise ValueError("role should be either 'sender' or 'receiver'")

        self.random_peer_sampling()

        route = [pd.DataFrame() for _ in range(n_layers)]
        view = self.peers_view.get().copy()

        converged_layers = [False for _ in range(n_layers)]
        # Converged when all layers are converged
        while not all(converged_layers):
            # Iteratively add one device per layer until converged
            for l_id in range(n_layers):
                # Skip this layer if converged
                if converged_layers[l_id]:
                    continue

                # If view is empty, exit
                if len(view) == 0:
                    break

                # Add a node to layer
                # By picking a device from view without replacement
                d = view.iloc[np.random.choice(len(view))]
                route[l_id] = route[l_id].append(d)
                view.drop(d.name, inplace=True)

                # Probability that all devices of layer will be offline
                p_failure = (1 - route[l_id]['p']).prod()
                # layer is converged when p_failure is below threshold
                converged_layers[l_id] = \
                    p_failure < self.conf['layer_threshold']

            if len(view) == 0:
                print("[build route] No more available nodes: "
                      "early abort.")
                break

        # In file_exchange, we ditch all info but the addresses
        for l_id in range(n_layers):
            route[l_id] = list(route[l_id]['addr'])

        return route

    def random_peer_sampling(self):
        self.peers_view.insert(
            self.global_view.get_sample(
                n=self.gossip_size,
                exclude_addr=self.addr))

    def is_online(self):
        return self.online.is_set()
