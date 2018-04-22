#!/usr/bin/env python3

# import numpy as np
from datetime import datetime, timedelta
from modules import config
from modules.network import Network
from modules.peers_view import PeersView
from modules.user import User
import pandas as pd
import random
import threading
import time


def run_experiments_set(N_LAYERS, LAYER_THRESHOLD, N_ROUNDS_SINCE_ROUTE,
                        N_ROUTES, N_EXPERIMENTS, PERIOD):
    routes_df = pd.DataFrame()
    layers_df = pd.DataFrame()

    period = PERIOD
    total_n_experiments = len(N_LAYERS) * len(LAYER_THRESHOLD)

    t_start = time.perf_counter()
    total_experiment_id = 1
    for n_layers in N_LAYERS:
        for layer_threshold in LAYER_THRESHOLD:
            experiments = [None] * N_EXPERIMENTS
            for experiment_id in range(N_EXPERIMENTS):
                n_users = n_layers * 5
                conf = {
                    'gossip_size': 10 * n_layers,
                    'layer_threshold': layer_threshold,
                    'minimum_node_availability': 0,
                    'n_layers': n_layers,  # must be odd
                    'n_rounds': N_ROUNDS_SINCE_ROUTE + 1,
                    'n_users': n_layers * 5,
                    'period': period,
                }

    #             layers, routes = run_experiment(conf, experiment_id,
    #                                            N_ROUTES,
    #                                            N_ROUNDS_SINCE_ROUTE)

                experiments[experiment_id] = Experiment(conf, experiment_id,
                                                        N_ROUTES,
                                                        N_ROUNDS_SINCE_ROUTE)
                experiments[experiment_id].start()

            for experiment in experiments:
                experiment.join()
                layers_df = layers_df.append(
                    experiment.layers_df, ignore_index=True)
                routes_df = routes_df.append(
                    experiment.routes_df, ignore_index=True)
                # not sure about this
                period = max(period, experiment.period)

            time_spent = timedelta(seconds=time.perf_counter() - t_start)
            print("[{}] Experiment {}/{} done.".format(
                time_spent, total_experiment_id, total_n_experiments))
            total_experiment_id += 1

    return layers_df, routes_df


def run_experiment(conf, experiment_id, n_routes, n_rounds_since_route):
    layers_df, routes_df = pd.DataFrame(), pd.DataFrame()
    users, net, address_book = init_experiment(conf)
    # perform a first round to pick devices
    _, period, _, _ = perform_round(conf, users)
    conf['period'] = max(conf['period'], period)

    # Putting (d1, d2) in a set to avoid duplicates
    devices_pairs = set()
    while len(devices_pairs) < n_routes:
        d1, d2 = get_devices_pair(users)
        devices_pairs.add((d1, d2))

    routes = [build_route(d1, d2, conf['n_layers'])
              for (d1, d2) in devices_pairs]

    for route_id, route in enumerate(routes):
        for layer_id, layer in enumerate(route):
            # print(layer)
            p_failure = 1
            if len(layer) > 0:
                p_failure = (1 - layer['p']).prod()
            layers_df = layers_df.append(pd.Series({
                'experiment_id': experiment_id,
                'route_id': route_id,
                'layer_id': layer_id,
                'n_layers': conf['n_layers'],
                'layer_threshold': conf['layer_threshold'],
                'layer_size': len(layer),
                'p_failure': p_failure
            }), ignore_index=True)

    for t in range(1, n_rounds_since_route+1):
        #         t_start = time.perf_counter()
        _, period, _, _ = perform_round(conf, users,
                                        current_round=t-1, sleep=True)
        conf['period'] = max(conf['period'], period)
#         t_end = time.perf_counter()
#         print("A round lasted {}".format(timedelta(seconds=t_end - t_start)))

        for route_id, route in enumerate(routes):
            success = False
            empty_layer = any([len(layer) == 0 for layer in route])
            if not empty_layer:
                success = all([
                    any([net.get_device(addr).is_online
                         for addr in layer['addr']])
                    for layer in route])

            routes_df = routes_df.append(pd.Series({
                'experiment_id': experiment_id,
                'route_id': route_id,
                'n_layers': conf['n_layers'],
                'layer_threshold': conf['layer_threshold'],
                't': t,
                'success': success
            }), ignore_index=True)

    return layers_df, routes_df, period


# Subclassing Thread to be able to retrieve dfs from the caller
class Experiment(threading.Thread):
    def __init__(self, conf, experiment_id, n_routes, n_rounds):
        super(Experiment, self).__init__()

        self.conf = conf
        self.experiment_id = experiment_id
        self.n_routes = n_routes
        self.n_rounds = n_rounds
        self.period = conf['period']

        self.routes_df, self.layers_df = pd.DataFrame(), pd.DataFrame()

    def run(self):
        self.layers_df, self.routes_df, self.period = \
            run_experiment(self.conf, self.experiment_id,
                           self.n_routes, self.n_rounds)


def init_experiment(conf=config.default):
    address_book = PeersView(conf)
    net = Network()

    n_devices = 0
    users = [None] * conf['n_users']
    for i in range(conf['n_users']):
        users[i] = User(address_book, net, conf)
        n_devices += users[i].n_devices

    #print("initialized {} users and {} devices".format(conf['n_users'], n_devices))
    return users, net, address_book


def perform_round(conf, users, address_book_df=None, devices_view_df=None,
                  current_round=None, sleep=False):
    t_start = datetime.now()
    # print("Round #{}/{} at {}".format(t+1,
    # conf['n_rounds'], datetime.now().time()))
    for user in users:
        user.act()
    for user in users:
        user.rps()

        if devices_view_df is not None:
            for d in user.devices:
                devices_view_df = devices_view_df.append(
                    d.peers_view.snapshot({'round': t}))
    if address_book_df is not None:
        address_book_df = address_book_df.append(
            address_book.snapshot({'round': t}))

    elapsed = conf['period']
    if sleep:
        elapsed = datetime.now() - t_start
        if elapsed > conf['period']:
            print("We are running overtime! Took {}, conf['period']={}".format(
                elapsed, conf['period']))
        elif current_round != conf['n_rounds'] - 1:
            #print("Sleeping", conf['period'] - elapsed)
            time.sleep((conf['period'] - elapsed).total_seconds())

    if current_round is None:
        current_round = 0
    else:
        current_round += 1

    return current_round, elapsed, address_book_df, devices_view_df


def get_online_device(users):
    user = random.choice(users)
    while not user.has_online_devices():
        user = random.choice(users)
    return user.get_online_device()


def get_devices_pair(users):
    d1, d2 = get_online_device(users), get_online_device(users)
    while d1.owner == d2.owner:
        d2 = get_online_device(users)
    return d1, d2


def build_route(d1, d2, n_layers):
    route = [None] * n_layers
    route[:n_layers//2] = d1.build_route(role='sender')
    route[n_layers//2:] = d1.build_route(role='receiver')
    return route
