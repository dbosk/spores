#!/usr/bin/env python3

import random
import string
from pandas.util import hash_pandas_object


def random_string(n):
    return ''.join(
        [random.choice(string.ascii_lowercase+string.digits)
         for _ in range(n)])


def hash_layer(df):
    return hash_pandas_object(df).sum()
