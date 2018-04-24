#!/usr/bin/env python3

import random
import string
from pandas.util import hash_pandas_object


NAMES = ['Cristy', 'Vickey', 'Sherie', 'Delilah', 'Rick', 'Denver', 'Stephany',
         'Many', 'Sandie', 'Deneen', 'Jesica', 'Newton', 'Maxwell', 'Sherrie',
         'Beatriz', 'Georgene', 'Herma', 'Mi', 'Bobbi', 'Julianna', 'Reita',
         'Kandi', 'Karlene', 'Lila', 'Nelly', 'Sibyl', 'Kermit', 'Luke',
         'Annabel', 'Moira', 'Hassie', 'Hilda', 'Vicki', 'Gloria', 'Kaci',
         'Dora', 'Gilbert', 'Livia', 'Buffy', 'Demetra', 'Barry', 'Lizzette',
         'Julius', 'Queen', 'Lyndsey', 'Lucy', 'Garnett',
         'Lavette', 'Magaly', 'Norene']


def random_name():
    return random.choice(NAMES)


def random_string(n):
    return ''.join(
        [random.choice(string.ascii_lowercase+string.digits)
         for _ in range(n)])


def hash_layer(df):
    return hash_pandas_object(df).sum()
