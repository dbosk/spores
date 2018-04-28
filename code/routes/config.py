#!/usr/bin/env python3

from datetime import timedelta

default = {
    'gossip_size': 20,
    'layer_threshold': 0.001,
    'minimum_node_availability': 0,
    'n_layers': 3,  # must be odd
    'n_rounds': 2,
    'n_users': 20,
    'period': timedelta(seconds=1),
}
