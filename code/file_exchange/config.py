#!/usr/bin/env python3

from datetime import timedelta

default = {
    'gossip_size': 20,
    'layer_threshold': 0.001,
    'minimum_node_availability': 0,
    'n_file_chunks': 10,
    'n_layers': 3,  # must be odd
    'file_size': 11,  # MB
    'chunk_max_size': 2  # MB, will depend on header size later
    'n_rounds': 2,
    'n_users': 20,
    'period': timedelta(seconds=1),
}
