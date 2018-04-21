#!/usr/bin/env python3

import pandas as pd
from datetime import timedelta, datetime
from . import config

COLUMNS = ["t", "addr", "type", "p"]


class PeersView:
    def __init__(self, conf=config.default):
        self.view = pd.DataFrame(columns=COLUMNS)
        self.conf = conf

    def put(self, t, addr, typ, p):
        self.view = self.view[self.view['addr'] != addr]

        self.view = self.view.append(
            pd.DataFrame({
                't': t,
                'addr': addr,
                'type': typ,
                'p': p
            }, index=[t])
        )

        self._prune_view()

    # Items is a dataframe
    def insert(self, items):
        if items is None:
            return

        self.view = self.view.append(items)
        self._prune_view()

    def get_sample(self, n=3, exclude_addr=None):
        view = self.view[self.view['addr'] != exclude_addr]

        if n > view.shape[0]:
            n = view.shape[0]
        if n == 0:
            return None

        return view.sample(n=n)

    def snapshot(self, additional_columns=None):
        if additional_columns is None:
            return self.view
        elif type(additional_columns) is dict:
            ret = self.view.copy()
            for k, v in additional_columns.items():
                ret[k] = v
            return ret
        else:
            raise ValueError(
                "additional_columns must be a dict of 'colname' -> 'value' "
                "to add the to the view")

    def _prune_view(self):
        # Time-bound
        expiration_limit = datetime.now() - self.conf['period']

        # print(self.view.index)
        self.view = self.view[self.view.index >= expiration_limit]
