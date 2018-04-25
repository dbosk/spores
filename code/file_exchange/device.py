#!/usr/bin/env python3

from . import config, peers_view, file, network
from .utils import random_string, hash_layer
from copy import deepcopy
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
        self.all_files_sent = True
        self.conf = conf
        self.death_requested = False
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
            # Wait until I'm online, with timeout
            # online.wait(0.1) return True only if online has been set
            while not self.online.wait(0.1):
                # Kill the device if death requested
                if self.death_requested and self.all_files_sent:
                    return

            # Kill the device if death requested
            if self.death_requested and self.all_files_sent:
                return

            # Send file chunks I am currently sharing
            self.share_files()

            # self.lock.acquire()
            # for f_id, file_info in self.sending_files.items():
            #     if file_info['f'].all_acknowledged():
            #         continue
            #         # We never remove a file from sending_files
            #         #del self.sending_files[f_id]

            #     self.send_chunk(file_info)

            #     if not self.is_online():
            #         break
            # self.lock.release()

            if not self.is_online():
                continue

            # Treat the messages in the queue
            while not self.message_queue.empty():
                m = self.message_queue.get()

                self.lock.acquire()
                # If my owner requested this file, update file state
                # and send acknowledgment
                if m.file_id in self.owner.receiving_files and \
                        m.type == network.MessType.CHUNK:

                    file_info = self.owner.receiving_files[m.file_id]
                    file_info['f'].shared(m.chunk_id)

                    print("{} (owned by {}) successfully received "
                          "file {}'s chunk #{}".format(
                              self.addr, self.owner.name,
                              m.file_id, m.chunk_id))

                    self.lock.release()
                    self.send_ack(file_info, m)

                elif m.file_id in self.owner.sending_files and \
                        m.type == network.MessType.ACK:

                    # This will update Device.sending_files[file_id] too
                    self.owner.sending_files[m.file_id]['f'].acknowledged(
                        m.chunk_id)

                    print("{} (owned by {}) successfully received ACK for "
                          "file {}'s chunk #{}".format(
                              self.addr, self.owner.name,
                              m.file_id, m.chunk_id))

                    if self.owner.sending_files[
                            m.file_id]['f'].all_acknowledged():
                        print("File sharing of "+m.file_id+" completed!")

                    self.lock.release()

                    # We never remove files from sending_files
                    # if file_info['f'].all_acknowledged():
                    #     del self.owner.sending_files[m.file_id]

                else:
                    self.lock.release()
                    self.send(m)

                if not self.is_online():
                    break

            # Release thread
            gevent.sleep(0)

    def please_die(self):
        self.death_requested = True

    # Called from the user's greenlet
    def update_state(self, is_online, p):
        self.lock.acquire()
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
        self.lock.release()

    def init_file_send(self, H_rdv_forward, H_rdv_backward, f):
        self.lock.acquire()
        # route = L_i + ... + L_j
        route = self.build_route("sender")
        # forward_route = (L_i + ... + L_j) + (L_RV + L_k + ... + L_l + L_B)
        forward_route = route + H_rdv_forward
        # backward_route = (L_l + ... + L_k + L_RV) + (L_j + ... + L_i) + L_A
        backward_route = H_rdv_backward + \
            route[::-1] + [self.owner.get_all_devices_addr()]

        print("Device {} (owned by {}) will send file {}".format(
            self.addr, self.owner.name, f.id))

        self.sending_files[f.id] = {
            'f': f,
            'forward_route': forward_route,
            'backward_route': backward_route,
        }
        self.lock.release()

        return self.sending_files[f.id]

    def share_files(self):
        if len(self.sending_files) == 0:
            return

        self.all_files_sent = all([
            file_info['f'].all_acknowledged()
            for file_info in self.sending_files.values()])
        if self.all_files_sent:
            return

        for f_id, file_info in self.sending_files.items():
            f = file_info['f']
            if f.all_acknowledged():
                continue
                # We never remove a file from sending_files
                # del self.sending_files[f_id]

            chunk_id = f.select_chunk()
            if chunk_id is None:
                raise Exception("None chunk_id, shouldn't be")

            m = network.Message(
                header=deepcopy(file_info['forward_route']),
                typ=network.MessType.CHUNK,
                file_id=f_id,
                chunk_id=chunk_id,
                size=f.chunks_size[chunk_id])

            # self.send(m)
            if self.send(m):
                f.shared(chunk_id)
                print("{} (owned by {}) successfully sent "
                      "file {}'s chunk #{}".format(
                          self.addr, self.owner.name,
                          f_id, chunk_id))

            if not self.is_online():
                return

    ### Messages exchange ###
    def receive(self, m):
        self.message_queue.put(m)

    def send_ack(self, file_info, m):
        m = network.Message(
            header=deepcopy(file_info['backward_route']),
            typ=network.MessType.ACK,
            file_id=m.file_id,
            chunk_id=m.chunk_id,
            size=self.conf['ack_size'])

        self.send(m)

    def send(self, m):
        d = self.net.get_device(random.choice(m.header[0]))

        # Rotate the headers so that next layer is at m.header[0]
        m.header = m.header[1:] + [m.header[0]]

        return network.emulate_transfer(
            d, m,
            self.conf['header_size'], self.conf['bandwidth'])

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

        if len(view) == 0:
            raise Exception("The view is empty")

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

    # def send_file_chunk(self, f):
    #     if f.all_shared():
    #         print("[Device.send_file_chunk]"
    #               " file {} already completed".format(
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
