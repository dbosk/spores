#!/usr/bin/env python3

import numpy as np


class File:
    def __init__(self, n_chunks, file_id):
        self.id = file_id
        self.n_chunks = n_chunks

        self.shared_chunks = np.array(
            [False for _ in range(n_chunks)], dtype=np.bool)

    def select_chunk(self):
        avail_chunks_id = np.argwhere(self.shared_chunks == False).ravel()

        if len(avail_chunks_id) == 0:
            return None

        return np.random.choice(avail_chunks_id)

    def ack(self, chunk_id):
        if chunk_id < 0 or chunk_id >= self.n_chunks:
            raise ValueError(
                "chunk_id ({}) should be in bounds [0, {}]".format(
                    chunk_id, self.n_chunks))

        self.shared_chunks[chunk_id] = True

    def all_shared(self):
        return all(shared_chunks)
