#!/usr/bin/env python3

import numpy as np

from common import load, load_output, save, score


def compute_row_pool_capacities(
    server_allocation, servers, rows, nbr_pools, row_cappa_list=None
):
    row_capacities = np.zeros([rows, nbr_pools], dtype=np.int)
    if row_cappa_list is not None:
        row_cappas = []
    for i in range(len(server_allocation)):
        if server_allocation[i]["row"] == -1:
            continue
        row_capacities[
            server_allocation[i]["row"], server_allocation[i]["pool_id"]
        ] += servers[i]["capacity"]
        if row_cappa_list == server_allocation[i]["row"]:
            row_cappas.append((i, servers[i]["capacity"]))
    if row_cappa_list is not None:
        return row_capacities, row_cappas
    return row_capacities


def best_pool2improve(rp_capacities, row):
    max_p = rp_capacities.max(axis=0)
    gc = rp_capacities.sum(axis=0) - max_p
    min_ps = np.argsort(gc)
    if np.all(max_p[min_ps[:-1]] == rp_capacities[row, min_ps[:-1]]):
        import pdb

        pdb.set_trace()
        max_diffs = max_p - rp_capacities[np.arange(rp_capacities.shape[0]) != row].max(
            axis=0
        )
        p_imp, p2_imp = np.argsort(max_diffs)[:2]
        inc = max_diffs[p2_imp] - max_diffs[p_imp] + 1
        return p_imp, inc

    for min_p, min_2_p in zip(min_ps[:-1], min_ps[1:]):
        if max_p[min_p] == rp_capacities[row, min_p]:
            continue
        inc_by = min(
            max_p[min_p] - rp_capacities[row, min_p], gc[min_2_p] - gc[min_p] + 1
        )
        return min_p, inc_by


def initialize_pool_ids(server_allocation, available, servers, nbr_pools):
    rp_capacities = np.zeros([available.shape[0], nbr_pools], dtype=np.int)
    for row in range(available.shape[0]):
        ids = [a["id"] for a in server_allocation if a["row"] == row]
        ids = sorted(ids, key=lambda i: servers[i]["capacity"])[::-1]
        for id in ids:
            p_capacities = rp_capacities.sum(axis=0)
            poss_min_idx = np.where(np.min(p_capacities) == p_capacities)[0]
            np.random.shuffle(poss_min_idx)
            p = poss_min_idx[0]
            # p = np.argmin(rp_capacities.sum(axis=0))
            server_allocation[id]["pool_id"] = p
            rp_capacities[row, p] += servers[id]["capacity"]


def improve_pool_ids(server_allocation, available, servers, nbr_pools, output_name):
    cur_score = score(server_allocation, available, servers, nbr_pools)
    rows = available.shape[0]
    while True:
        shuffled_row_ids = np.arange(rows)
        np.random.shuffle(shuffled_row_ids)
        for row in shuffled_row_ids:
            rp_capacities, r_c_list = compute_row_pool_capacities(
                server_allocation, servers, rows, nbr_pools, row_cappa_list=row
            )
            r_c_list = sorted(r_c_list, key=lambda x: x[1])[::-1]
            rp_capacities[0] = 0
            while len(r_c_list):
                p_imp, inc_by = best_pool2improve(rp_capacities, row)
                if r_c_list[-1][1] > inc_by:
                    sel_r_c_idx = -1
                else:
                    for i, (r_c_server_id, r_c_cappa) in enumerate(r_c_list):
                        if r_c_cappa <= inc_by:
                            sel_r_c_idx = i
                            break
                rp_capacities[row, p_imp] += r_c_list[sel_r_c_idx][1]
                server_allocation[r_c_list[sel_r_c_idx][0]]["pool_id"] = p_imp
                del r_c_list[sel_r_c_idx]
            # compute score
            new_score = score(server_allocation, available, servers, nbr_pools)
            if new_score > cur_score:
                cur_score = new_score
                save(
                    server_allocation,
                    available,
                    servers,
                    nbr_pools,
                    output_name="improved_%s" % output_name,
                )


if __name__ == "__main__":
    output_name = "solution_dummy_000218_160011"
    inputs = load(example=False)
    server_allocation = load_output(output_name + ".out")
    for i in range(len(server_allocation)):
        server_allocation[i]["id"] = i
    initialize_pool_ids(server_allocation, *inputs)
    save(server_allocation, *inputs, output_name="pool_init_%s" % output_name)
    # improve_pool_ids(server_allocation, *inputs, output_name=output_name)
