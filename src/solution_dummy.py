#!/usr/bin/env python3

import pathlib
import numpy as np
from src.common import load
import itertools


def solution_dummy():
    available, servers, p = load(example=True)

    # available_servers = np.ones(shape=(len(servers), ), dtype=np.bool)

    servers_with_ratio = [{**x, 'ratio': x['capacity'] / x['size']} for x in servers]
    servers_by_ratio = sorted(servers_with_ratio, key=lambda i: i['ratio'],
                              reverse=True)

    free_slots = []
    free_slot_starts = []
    starts = np.diff(np.concatenate((np.zeros(shape=(available.shape[0], 1), dtype=np.int32),
                                     available.astype(np.int32)), axis=-1))

    free_slot_indices = []

    for i, (row, s) in enumerate(zip(available, starts)):
        free_slot_lengths = [
            sum(1 for _ in group) for key, group in itertools.groupby(row) if key
        ]
        free_slots.append(free_slot_lengths)
        indices = np.argwhere(s)
        indices = np.stack((np.repeat(i, indices.shape[0]), indices[..., 0]), axis=1)
        free_slot_indices.append(indices)

    free_slot_lengths = np.concatenate(free_slots, axis=0)
    free_slot_indices = np.concatenate(free_slot_indices, axis=0)

    def use_slot(index, serversize, server_dict):
        server_dict['row'] = free_slot_indices[index, 0]
        server_dict['left_slot'] = free_slot_indices[index, 1]

        if serversize == free_slot_lengths[index]:
            np.delete(free_slot_lengths, index, 0)
            np.delete(free_slot_indices, index, 0)
        else:
            free_slot_lengths[index] -= serversize
            free_slot_indices[index, 1] += serversize

    pool_count = 0
    for server in servers_by_ratio:
        if server['size'] > np.max(free_slots):
            server['row'] = -1
            server['left_slot'] = -1
            server['pool_id'] = -1
            continue

        exact_fits = free_slot_lengths == server['size']
        if np.any(exact_fits):
            use_slot(index=np.argwhere(exact_fits)[0, 0], serversize=server['size'],
                     server_dict=server)
        else:
            larger_fits = free_slot_lengths > server['size']
            use_slot(index=np.argwhere(larger_fits)[0, 0], serversize=server['size'],
                     server_dict=server)

        server['pool_id'] = pool_count % p
        pool_count += 1

    return servers_by_ratio


if __name__ == "__main__":
    solution_dummy()
