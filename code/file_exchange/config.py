#!/usr/bin/env python3

from datetime import timedelta

default = {
    'ack_size': 0,  # MB
    'bandwidth': 10,  # MB/s
    'chunk_max_size': 2,  # MB, will depend on header size later
    'file_size': 11,  # MB
    'gossip_size': 20,
    'header_size': 0.1,  # MB, will depend on #devices/layers later
    'layer_threshold': 0.001,
    'minimum_node_availability': 0,
    'output_dir': 'outputs/file_exchange/',
    'do_monitor': True,
    'n_file_chunks': 10,
    'n_layers': 3,  # must be odd
    'n_rounds': 2,
    'n_users': 20,
    'n_file_exchanges': 10,
    'period': timedelta(seconds=1),  # don't put milliseconds!
    'send_strategy': 'random',  # 'random' or 'random_connected'
}
