#!/usr/bin/env python3

from itertools import groupby

from common import load, save

# import matplotlib.pyplot as plt
# import numpy as np


available, servers, nbr_pools = load(example=False)
rows = available.shape[0]
free_slots = available.sum()
ratio_sorted_servers = sorted(
    servers, key=lambda x: (-x["capacity"] / x["size"], x["size"])
)


print("nbr servers:", len(servers))


def get_row_wise_slot_lengths(available_slots):
    result_lengths = []
    result_starts = []
    for i in range(available_slots.shape[0]):
        row_result_lengths = []
        row_result_starts = []
        count = 0
        for k, g in groupby(available_slots[i]):
            n = len(list(g))
            if k:
                row_result_lengths.append(n)
                row_result_starts.append(count)
            count += n
        assert count == available_slots.shape[1]
        result_lengths.append(row_result_lengths)
        result_starts.append(row_result_starts)
    return result_lengths, result_starts


def est_gc_in_optimal_distribution_case(list_capas):
    if len(list_capas) == 0:
        return 0
    list_capas = sorted(list_capas)
    if len(list_capas) > rows:
        merges_needed = len(list_capas) - rows
        assert merges_needed * 2 <= len(list_capas)
        mergers = list_capas[: 2 * merges_needed]
        merged = [
            a + b
            for a, b in zip(mergers[:merges_needed], mergers[::-1][:merges_needed])
        ]
        list_capas = merged + list_capas[2 * merges_needed :]
    assert len(list_capas) <= rows
    return sum(list_capas) - max(list_capas)


def get_other_optimal_servers(throw_away_large):
    selected = sorted(servers, key=lambda s: (-s["size"], s["capacity"]))
    deselected = selected[:throw_away_large]
    selected = selected[throw_away_large:]
    # plt.figure()
    # plt.scatter(
    #     [s["size"] + np.random.normal() * 0.01 for s in selected],
    #     [s["capacity"] + np.random.normal() * 0.1 for s in selected],
    #     s=1,
    # )
    # plt.scatter(
    #     [s["size"] + np.random.normal() * 0.01 for s in deselected],
    #     [s["capacity"] + np.random.normal() * 0.1 for s in deselected],
    #     s=1,
    # )
    # plt.show()

    selected = sorted(selected, key=lambda s: (-s["capacity"] / s["size"], s["size"]))
    used_slots = 0
    final_selection = []
    final_deselection = deselected
    for server in selected:
        if used_slots + server["size"] <= free_slots:
            final_selection.append(server)
            used_slots += server["size"]
        else:
            final_deselection.append(server)
    # plt.figure()
    # plt.scatter(
    #     [s["size"] + np.random.normal() * 0.01 for s in selected],
    #     [s["capacity"] + np.random.normal() * 0.1 for s in selected],
    #     s=1,
    # )
    # plt.scatter(
    #     [s["size"] + np.random.normal() * 0.01 for s in deselected],
    #     [s["capacity"] + np.random.normal() * 0.1 for s in deselected],
    #     s=1,
    # )
    # plt.show()
    return final_selection


def get_optimal_servers(at_least_nbr_servers=100):
    selected = []
    deselected = [*ratio_sorted_servers]
    used_slots = 0
    target_avg = free_slots / at_least_nbr_servers
    while len(selected) < at_least_nbr_servers or free_slots - used_slots > 0:
        cur_l = len(selected)
        for i in range(len(deselected)):
            if (used_slots + deselected[i]["size"]) / (
                len(selected) + 1
            ) > target_avg or (used_slots + deselected[i]["size"]) > free_slots:
                continue
            used_slots += deselected[i]["size"]
            selected.append(deselected[i])
            del deselected[i]
            break
        if cur_l == len(selected):
            break
    print("target avg (slots/server)", target_avg)
    print("reached", used_slots / len(selected))
    # plt.figure()
    # plt.scatter(
    #     [s["size"] + np.random.normal() * 0.01 for s in selected],
    #     [s["capacity"] + np.random.normal() * 0.1 for s in selected],
    #     s=1,
    # )
    # plt.scatter(
    #     [s["size"] + np.random.normal() * 0.01 for s in deselected],
    #     [s["capacity"] + np.random.normal() * 0.1 for s in deselected],
    #     s=1,
    # )
    # plt.show()
    return selected


def put_servers_in_pools(server_list, nbr_pools):
    pools = [([], []) for _ in range(nbr_pools)]
    server_list = sorted(server_list, key=lambda x: -x["capacity"])
    gc_threshold = 416
    for server in server_list:
        # first check if you can place with greatest gain without going over gc threshold
        pools = sorted(
            pools,
            key=lambda p: (
                gc_threshold
                < est_gc_in_optimal_distribution_case(p[0] + [server["capacity"]]),
                est_gc_in_optimal_distribution_case(p[0])
                - est_gc_in_optimal_distribution_case(p[0] + [server["capacity"]]),
                len(p[0]),
            ),
        )
        if gc_threshold < est_gc_in_optimal_distribution_case(
            pools[0][0] + [server["capacity"]]
        ):
            # first check failed, so now we want to put it to improve the weakest
            pools = sorted(
                pools,
                key=lambda p: (
                    est_gc_in_optimal_distribution_case(p[0]),
                    sum(p[0]),
                    len(p[0]),
                ),
            )
        idx = 0
        pools[idx] = (pools[idx][0] + [server["capacity"]], pools[idx][1] + [server])
    # print(pools)
    return pools


def allocate_servers_to_rows(pool_assignment):
    def gc_loss_if_missing(pool, pool_row_servers):
        assert len(pool) <= rows
        capas = []
        for cur_pool_row_servers in pool:
            capas.append(
                sum(pool_server["capacity"] for pool_server in cur_pool_row_servers)
            )
        assert len(capas) == len(pool)
        pool_row_servers_capa = sum(
            servers[pool_server["id"]]["capacity"] for pool_server in pool_row_servers
        )
        assert pool_row_servers_capa in capas
        total_before_missing = sum(capas) - max(capas)
        capas_missing = capas
        del capas_missing[capas.index(pool_row_servers_capa)]
        total_if_missing = sum(capas_missing) - max(capas_missing)
        assert total_if_missing < total_before_missing
        return total_before_missing - total_if_missing

    def score(gc_loss_if_missing, sizes, nbr_pool_rows):
        assert nbr_pool_rows <= rows
        is_close_to_rows = nbr_pool_rows >= rows - 2
        has_large_block = any(s >= 4 for s in sizes)
        has_many_rows = nbr_pool_rows >= rows - 8
        has_medium_sized_blocks = any(s >= 2 for s in sizes)
        return (
            is_close_to_rows,
            has_large_block,
            has_medium_sized_blocks,
            sum(sizes),
            has_many_rows,
            gc_loss_if_missing,
        )
        # return (nbr_pool_rows, sum(sizes) - len(sizes), len(sizes), gc_loss_if_missing)

    # agg servers in pool_assignment by row_agg_rule
    assert nbr_pools == len(pool_assignment)
    for i in range(nbr_pools):
        pool = pool_assignment[i]
        if len(pool) <= rows:
            pool_assignment[i] = [[s] for s in pool]
            continue
        nbr_merges = len(pool) - rows
        assert nbr_merges * 2 <= len(pool)
        pool = sorted(pool, key=lambda s: (s["capacity"], s["size"]))
        merges = [
            [a, b]
            for a, b in zip(pool[:nbr_merges], pool[nbr_merges : 2 * nbr_merges][::-1])
        ]
        rest_pool = [[s] for s in pool[2 * nbr_merges :]]
        pool_assignment[i] = merges + rest_pool

    server_allocation = []
    for pool_id, pool in enumerate(pool_assignment):
        for pool_row_servers in pool:
            cur = []
            for pool_server in pool_row_servers:
                cur.append({"id": pool_server["id"], "pool_id": pool_id})
            server_allocation.append(cur)

    server_allocation = sorted(
        server_allocation,
        key=lambda pool_row_servers: score(
            gc_loss_if_missing(
                pool_assignment[pool_row_servers[0]["pool_id"]], pool_row_servers
            ),
            [servers[s["id"]]["size"] for s in pool_row_servers],
            len(pool_assignment[pool_row_servers[0]["pool_id"]]),
        ),
    )[::-1]

    def servers_fit(slot_lengths, some_servers):
        if len(slot_lengths) == 0:
            return False
        if len(some_servers) == 1:
            return any(
                length >= servers[some_servers[0]["id"]]["size"]
                for length in slot_lengths
            )
        else:
            assert len(some_servers) == 2
            sizes = [servers[s["id"]]["size"] for s in some_servers]
            if any(length >= sum(sizes) for length in slot_lengths):
                return True
            slot_lengths = sorted(slot_lengths)
            sizes = sorted(sizes)
            if len(slot_lengths) <= 1:
                return False
            return slot_lengths[-2] >= sizes[0] and slot_lengths[-1] >= sizes[1]

    pools_in_rows = [set() for _ in range(rows)]
    available_slots = available.copy()
    row_wise_slot_lengths, start_row_wise_cont_slots = get_row_wise_slot_lengths(
        available_slots
    )
    print(sum(map(sum, row_wise_slot_lengths)))
    print(
        sum(
            map(lambda sl: sum(servers[s["id"]]["size"] for s in sl), server_allocation)
        )
    )
    print(free_slots)
    assert sum(map(sum, row_wise_slot_lengths)) == sum(
        map(lambda sl: sum(servers[s["id"]]["size"] for s in sl), server_allocation)
    )
    for pool_row_servers in server_allocation:
        # find a suitable row, based on current pool not beeing in that row ...
        pool_id = pool_row_servers[0]["pool_id"]
        suitable_rows = [k for k in range(rows) if pool_id not in pools_in_rows[k]]
        assert len(suitable_rows) > 0, "there seems to be to many pool rows"
        # ... and the row having enough space
        suitable_rows = [
            k
            for k in suitable_rows
            if servers_fit(row_wise_slot_lengths[k], pool_row_servers)
        ]
        assert len(suitable_rows) > 0, "no space to fit the servers anymore"
        # ... and sort by row with most space
        suitable_rows = sorted(
            suitable_rows, key=lambda r: -sum(row_wise_slot_lengths[r])
        )
        selected_row = suitable_rows[0]
        pools_in_rows[selected_row].add(pool_id)

        # now do the placing
        for pool_server in sorted(
            pool_row_servers, key=lambda s: -servers[s["id"]]["size"]
        ):
            cur_size = servers[pool_server["id"]]["size"]
            best_slot_size = sorted(
                row_wise_slot_lengths[selected_row], key=lambda sl: (sl < cur_size, sl)
            )[0]
            cont_slot_idx = row_wise_slot_lengths[selected_row].index(best_slot_size)
            pool_server["left_slot"] = start_row_wise_cont_slots[selected_row][
                cont_slot_idx
            ]
            pool_server["row"] = selected_row
            start_row_wise_cont_slots[selected_row][cont_slot_idx] += cur_size
            row_wise_slot_lengths[selected_row][cont_slot_idx] -= cur_size
    return server_allocation


print(nbr_pools * available.shape[0])
print(len(servers) - 80)

optimal_servers = get_other_optimal_servers(0)
# get_optimal_servers(1)
print("nbr pools", nbr_pools)
print("selected servers", len(optimal_servers))
print("used slots", sum(s["size"] for s in optimal_servers))
print("free slots", free_slots)
sum_capa = sum(s["capacity"] for s in optimal_servers)
print("total capacity", sum_capa)
print("best case score", sum_capa / nbr_pools * (rows - 1) / rows)
pool_assignment = put_servers_in_pools(optimal_servers, nbr_pools)
pool_assignment = [p[1] for p in pool_assignment]
print("selected servers after pool assignment", sum(map(len, pool_assignment)))
print(
    "recompute used slots",
    sum([sum([p["size"] for p in pool]) for pool in pool_assignment]),
)

min_gc = 1e6
sum_sizes_after_pool_assignment = 0
for i, pool_servers in enumerate(pool_assignment):
    capas = [s["capacity"] for s in pool_servers]
    sum_sizes_after_pool_assignment += sum(s["size"] for s in pool_servers)
    print()
    print("pool id", i)
    print("nbr servers", len(pool_servers))
    print("capas", capas)
    est_gc = est_gc_in_optimal_distribution_case(capas)
    min_gc = min(min_gc, est_gc)
    print("sum capas", sum(capas))
    print("est gc", est_gc)
    print("sum sizes", sum(s["size"] for s in pool_servers))
print(min_gc)
assert sum_sizes_after_pool_assignment == free_slots

server_allocation = allocate_servers_to_rows(pool_assignment)
flat_server_allocation = sum(server_allocation, [])

save(
    flat_server_allocation, available, servers, nbr_pools, output_name="after_solution"
)
