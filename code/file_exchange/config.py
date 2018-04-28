#!/usr/bin/env python3

from datetime import timedelta

EXPERIMENT_NAME = 'default'
default = {
    'ack_size': 0,  # kB
    'bandwidth': 128,  # kB/s
    'chunk_max_size': 512,  # kB, will depend on header size later
    'do_monitor': True,
    'experiment_id': 0,
    'experiment_name': EXPERIMENT_NAME,
    'gossip_size': 20,
    'header_size': 100,  # kB, will depend on #devices/layers later
    'layer_threshold': 0.001,
    'min_file_size': 51200,  # kB
    'max_file_size': 51200,  # kB
    'minimum_node_availability': 0,
    'n_file_exchanges': 10,
    'n_layers': 3,  # must be odd
    'n_rounds': 2,
    'n_users': 20,
    'output_dir': 'data/'+EXPERIMENT_NAME+'/',
    'period': timedelta(seconds=1),  # don't put milliseconds!
    'ping_time': 0.1,  # s
    'send_strategy': 'random',  # 'random' or 'random_connected'
}
