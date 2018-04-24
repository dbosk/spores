#!/usr/bin/env python3

import pandas as pd
from datetime import timedelta, datetime
from . import config
from gevent.lock import Semaphore

COLUMNS = ["t", "addr", "type", "p"]


class PeersView:
    def __init__(self, conf=config.default):
        self._view = pd.DataFrame(columns=COLUMNS)
        self.conf = conf
        self.lock = Semaphore()

    def put(self, t, addr, typ, p):
        self.lock.acquire()
        # Remove previous entry for addr if any
        self._view = self._view[self._view['addr'] != addr]

        # Add the new line
        self._view = self._view.append(
            pd.DataFrame({
                't': t,
                'addr': addr,
                'type': typ,
                'p': p
            }, index=[t])
        )

        # We prune on reads, not writes
        # self._prune_view()
        self.lock.release()

    # Items is a dataframe
    def insert(self, items):
        if items is None:
            return

        self.lock.acquire()
        self._view = self._view.append(items)

        # We prune on reads, not writes
        # self._prune_view()
        self.lock.release()

    def get(self):
        self.lock.acquire()
        self._prune_view()
        ret = self._view.copy()
        self.lock.release()
        return ret

    def get_sample(self, n=3, exclude_addr=None):
        self.lock.acquire()
        self._prune_view()
        view = self._view[self._view['addr'] != exclude_addr]

        if n > view.shape[0]:
            n = view.shape[0]
        if n == 0:
            self.lock.release()
            return None

        # Sample returns a copy of df, not a slice
        ret = view.sample(n=n)
        self.lock.release()

        return ret

    def snapshot(self, additional_columns=None):
        self.lock.acquire()
        self._prune_view()
        ret = self._view.copy()
        self.lock.release()

        if additional_columns is None:
            return ret
        elif type(additional_columns) is dict:
            for k, v in additional_columns.items():
                ret[k] = v
            return ret
        else:
            raise ValueError(
                "additional_columns must be a dict of 'colname' -> 'value' "
                "to add the to the view")

    # Must be called inside lock
    def _prune_view(self):
        # Time-bound
        expiration_limit = datetime.now() - self.conf['period']

        # print(self._view.index)
        self._view = self._view[self._view.index >= expiration_limit]
