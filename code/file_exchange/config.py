#!/usr/bin/env python3

from datetime import timedelta

EXPERIMENT_NAME = 'default'
default = {
    'ack_size': 0,  # kB
    'bandwidth': 400,  # kB/s
    'chunk_max_size': 128,  # kB, will depend on header size later
    'file_size': 10240,  # kB
    'gossip_size': 20,
    'header_size': 100,  # kB, will depend on #devices/layers later
    'layer_threshold': 0.001,
    'minimum_node_availability': 0,
    'experiment_name': EXPERIMENT_NAME,
    'output_dir': 'data/'+EXPERIMENT_NAME+'/',
    'do_monitor': True,
    'n_file_chunks': 10,
    'n_layers': 3,  # must be odd
    'n_rounds': 2,
    'n_users': 20,
    'n_file_exchanges': 10,
    'period': timedelta(seconds=1),  # don't put milliseconds!
    'ping_time': 0.1,  # s
    'send_strategy': 'random',  # 'random' or 'random_connected'
}
