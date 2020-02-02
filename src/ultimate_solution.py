#!/usr/bin/env python3

import numpy as np
import datetime
from src.common import load, save


def get_available_index(bool_array):
    if np.count_nonzero(bool_array) > 0:
        random_pool_idx = np.random.random_integers(low=0, high=bool_array.size-1)
        while not bool_array[random_pool_idx]:
            random_pool_idx = np.random.random_integers(low=0, high=bool_array.size-1)
        return random_pool_idx
    else:
        return -1


def find_subsequence(seq, subseq):
    target = np.dot(subseq, subseq)
    candidates = np.where(np.correlate(seq,
                                       subseq, mode='valid') == target)[0]
    # some of the candidates entries may be false positives, double check
    check = candidates[:, np.newaxis] + np.arange(len(subseq))
    mask = np.all((np.take(seq, check) == subseq), axis=-1)
    return candidates[mask]


def get_first_available_slot_with_sufficient_size(row_availability_mask, server_size):
    if np.count_nonzero(row_availability_mask) < server_size:
        return -1
    else:
        candidates = find_subsequence(row_availability_mask, np.ones([server_size],dtype=np.bool))
        if candidates.size > 0:
            return candidates[0]
        else:
            return -1


def main():
    input_stuff = load(False)
    available, servers, num_pools = load(False)
    print(servers)
    max_iterations = 1e6
    num_it = 0
    server_available_for_placement = np.ones([len(servers)], dtype=np.bool)

    solution = []
    while np.count_nonzero(available) > 0 and num_it < max_iterations and np.count_nonzero(server_available_for_placement) > 0:
        random_server_idx = get_available_index(server_available_for_placement)

        if random_server_idx < 0:
            print("All servers allocated!")
            break
        else:
            pass

        random_row_idx = np.random.random_integers(low=0, high=available.shape[0]-1)
        first_suitable_index = get_first_available_slot_with_sufficient_size(available[random_row_idx], servers[random_server_idx]["size"])

        if first_suitable_index < 0:
            pass
        else:
            server_available_for_placement[random_server_idx] = False
            available[random_row_idx, first_suitable_index:first_suitable_index+servers[random_server_idx]["size"]] = False
            random_pool_idx = np.random.random_integers(low=0, high=num_pools-1)
            sol_entry = {}
            sol_entry["left_slot"] = first_suitable_index
            sol_entry["row"] = random_row_idx
            sol_entry["server_id"] = random_server_idx
            sol_entry["pool_id"] = random_pool_idx
            solution.append(sol_entry)

        num_it += 1
    print(solution)

    save(solution, *input_stuff, output_name="ultimate_solution")

if __name__ == '__main__':
    main()