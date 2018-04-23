#!/usr/bin/env python3

import pandas as pd
from datetime import timedelta, datetime

COLUMNS = ["t", "addr", "p"]


class PeersView:
    def __init__(self, expiration_period=timedelta(seconds=1)):
        self.view = pd.DataFrame(columns=COLUMNS)

        self.expiration_period = expiration_period

    def put(self, t, addr, p, prune=True):
        self.view = self.view[self.view['addr'] != addr]

        self.view = self.view.append(
            pd.DataFrame({
                't': t,
                'addr': addr,
                'p': p
            }, index=[t])
        )

        if prune:
            self._prune_view()

    # Items is a dataframe
    def insert(self, items):
        if len(items) == 0:
            return
        # print("insert:")
        # print(type(items))
        # print(items)

        for _, item in items.iterrows():
            self.put(item['t'], item['addr'], item['p'], prune=False)

        self._prune_view()

    def get_sample(self, n=3, exclude_addr=None):
        view = self.view[self.view['addr'] != exclude_addr]

        if n > view.shape[0]:
            n = view.shape[0]
        if n == 0:
            return []

        return view.sample(n=n)

    def _prune_view(self):
        # Time-bound
        expiration_limit = datetime.now() - self.expiration_period

        # print(self.view.index)
        self.view = self.view[self.view.index >= expiration_limit]
