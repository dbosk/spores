#!/usr/bin/env python3

from copy import deepcopy
import numpy as np
from .utils import random_string


FILE_ID_SIZE = 6


# We use this class to represent files to share and files to receive
class File:
    def __init__(self, size, chunk_max_size):
        self.id = random_string(FILE_ID_SIZE)
        self.size = size

        # Computing size of chunks
        self.chunks_size = []
        while size > 0:
            chunk_size = min(size, chunk_max_size)
            size -= chunk_size
            self.chunks_size.append(chunk_size)

        self.n_chunks = len(self.chunks_size)

        # Chunks either sent or received
        # uint to count the number of times chunk was sent
        self.shared_chunks = np.array(
            [0 for _ in range(self.n_chunks)], dtype=np.uint)
        # Chunks acknowledged (only for sender)
        self.acked_chunks = self.shared_chunks.astype(np.bool)

    # Used by sender to pick right chunk to send
    def select_chunk(self):
        unsent_chunks_id = np.argwhere(self.shared_chunks == 0).ravel()

        # If there are chunks we did not send yet, pick among them randomly
        if len(unsent_chunks_id) > 0:
            return np.random.choice(unsent_chunks_id)

        # Get ids of chunks not acked
        not_acked_chunks_id = np.argwhere(self.acked_chunks == False).ravel()

        # Wooo, all sent and all acknowledged
        if len(not_acked_chunks_id) == 0:
            return None

        # If all chunks were sent at least once
        # Return the chunk_id that was sent the least but did not get an ack
        for x in self.shared_chunks.argsort():
            if x in not_acked_chunks_id:
                return x

    # Receiver: this chunk was received
    # Sender: this chunk was sent
    def shared(self, chunk_id):
        if chunk_id < 0 or chunk_id >= self.n_chunks:
            raise ValueError(
                "chunk_id ({}) should be in bounds [0, {}]".format(
                    chunk_id, self.n_chunks))

        self.shared_chunks[chunk_id] += 1

    # Sender: received ack for this chunk
    def acknowledged(self, chunk_id):
        if chunk_id < 0 or chunk_id >= self.n_chunks:
            raise ValueError(
                "chunk_id ({}) should be in bounds [0, {}]".format(
                    chunk_id, self.n_chunks))

        self.acked_chunks[chunk_id] = True

    def all_shared(self):
        return all(self.shared_chunks)

    def all_acknowledged(self):
        return all(self.acked_chunks)

    def copy(self):
        return deepcopy(self)
