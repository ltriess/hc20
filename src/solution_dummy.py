#!/usr/bin/env python3

import pathlib
import numpy as np
from src.common import load, save
import itertools


def solution_dummy(available, servers, p, shuffle_free_positions: bool = False):
    # available_servers = np.ones(shape=(len(servers), ), dtype=np.bool)

    servers_with_ratio = [{**x, "ratio": x["capacity"] / x["size"]} for x in servers]
    servers_by_ratio = sorted(
        servers_with_ratio, key=lambda i: i["ratio"], reverse=True
    )

    free_slots = []
    free_slot_starts = []
    starts = np.diff(
        np.concatenate(
            (
                np.zeros(shape=(available.shape[0], 1), dtype=np.int32),
                available.astype(np.int32),
            ),
            axis=-1,
        )
    )
    starts = starts == 1

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

    if shuffle_free_positions:
        # SHUFFLE
        slot_indices = np.arange(0, free_slot_lengths.shape[0])
        np.random.shuffle(slot_indices)
        free_slot_lengths = free_slot_lengths[slot_indices]
        free_slot_indices = free_slot_indices[slot_indices]

    def use_slot(index, serversize, server_dict, lengths, indices):
        server_dict["row"] = indices[index, 0]
        server_dict["left_slot"] = indices[index, 1]

        if serversize == lengths[index]:
            updated_lengths = np.delete(lengths, index, 0)
            updated_indices = np.delete(indices, index, 0)
        else:
            lengths[index] -= serversize
            indices[index, 1] += serversize
            updated_lengths = lengths
            updated_indices = indices

        return updated_lengths, updated_indices

    pool_count = 0
    for server in servers_by_ratio:
        if free_slot_lengths.size == 0 or server["size"] > np.max(free_slot_lengths):
            server["row"] = -1
            server["left_slot"] = -1
            server["pool_id"] = -1
            continue

        exact_fits = free_slot_lengths == server["size"]
        if np.any(exact_fits):
            free_slot_lengths, free_slot_indices = use_slot(
                index=np.argwhere(exact_fits)[0, 0],
                serversize=server["size"],
                server_dict=server,
                lengths=free_slot_lengths,
                indices=free_slot_indices,
            )
        else:
            larger_fits = free_slot_lengths > server["size"]
            assert np.any(larger_fits)
            free_slot_lengths, free_slot_indices = use_slot(
                index=np.argwhere(larger_fits)[0, 0],
                serversize=server["size"],
                server_dict=server,
                lengths=free_slot_lengths,
                indices=free_slot_indices,
            )
        server["pool_id"] = pool_count % p
        pool_count += 1

    print(
        "Used capacity: {}".format(
            sum([x["capacity"] for x in servers_by_ratio if x["row"] != -1])
        )
    )

    capacity_per_row = np.zeros((16,), np.int32)
    for r in range(available.shape[0]):
        capacity_per_row[r] = sum(
            [x["capacity"] for x in servers_by_ratio if x["row"] == r]
        )
    print(capacity_per_row)

    return servers_by_ratio


if __name__ == "__main__":
    available, servers, p = load(example=False)
    server_dict = solution_dummy(available, servers, p)
    save(server_dict, available, servers, p, "solution_dummy")
