#!/usr/bin/env python3

import random
import string
from pandas.util import hash_pandas_object
import gevent


NAMES = ['Cristy', 'Vickey', 'Sherie', 'Delilah', 'Rick', 'Denver', 'Stephany',
         'Many', 'Sandie', 'Daniel', 'Jessica', 'Newton', 'Maxwell', 'Morty',
         'Beatriz', 'Georgene', 'Herma', 'Mi', 'Bobbi', 'Julianna', 'Reita',
         'Kandi', 'Karlene', 'Lila', 'Nelly', 'Sibyl', 'Kermit', 'Luke',
         'Annabel', 'Moira', 'Hassie', 'Gilda', 'Vicki', 'Gloria', 'Kaci',
         'Dora', 'Gilbert', 'Livia', 'Buffy', 'Demetra', 'Barry', 'Lizzette',
         'Julius', 'Queen', 'Lyndsey', 'Lucy', 'Garnett', 'Lavette', 'Magaly',
         'Norene', 'Toshiko', 'Maurita', 'Angelika', 'Ann', 'Bennie',
         'Randolph', 'Temika', 'Evelyne', 'Betty', 'Athena', 'Shawnda',
         'Magdalen', 'Benjamin', 'Lorine', 'Morgan', 'Tim', 'Elinor', 'Cordia',
         'Jay Z', 'Brian', 'Broderick', 'Janis', 'Nadia', 'Delaine', 'Vonnie',
         'Adaline', 'Leigh', 'Consuelo', 'Patty', 'Isaura', 'Elvera', 'Jack',
         'Cristina', 'Charissa', 'Kaylee', 'Britany', 'Jayne', 'Yuriko',
         'Annelle', 'Twila', 'January', 'Jillian', 'Jean Panda', 'Daisy', 'Mazie',
         'Bronwyn', 'Otha', 'Shane', 'Brande', 'Renna']


def random_name():
    return random.choice(NAMES)


def random_string(n):
    return ''.join(
        [random.choice(string.ascii_lowercase+string.digits)
         for _ in range(n)])


def hash_layer(df):
    return hash_pandas_object(df).sum()