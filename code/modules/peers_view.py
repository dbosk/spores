#!/usr/bin/env python3

import pandas as pd

COLUMNS = ["t", "addr", "p"]


class PeersView:
    def __init__(self, max_size):
        self.view = pd.DataFrame(columns=COLUMNS)
        self.max_size = max_size

    def put(self, t, addr, p, prune=True):
        self.view = self.view[self.view['addr'] != addr]

        self.view = self.view.append(
            pd.DataFrame({
                't': t,
                'addr': addr,
                'p': p
            }, index=[t])
        )

        self._prune_view()

    def insert(self, items):
        for item in items:
            self.put(*item, prune=False)

        self._prune_view()

    def get_sample(self, n=3):
        if n > self.view.shape[0]:
            n = self.view.shape[0]

        return self.view.sample(n=n).values

    def _prune_view(self):
        if self.view.shape[0] > self.max_size:
            self.view = self.view[self.view.shape[0] - self.max_size:]
