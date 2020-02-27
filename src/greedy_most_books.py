#!/usr/bin/env python3


import numpy as np

from common import load, save


def compute_nbr_books_processable_nbr_points_makeable_idle_time(
    lib, days_left: int, books_to_scan_left: set, scores: list, quantile: float
):
    days_left -= lib["t"]
    max_books = max(days_left * lib["m"], 0)
    interesting_books_in_lib = lib["ids"] & books_to_scan_left
    nbr_books_processable = min(max_books, len(interesting_books_in_lib))
    logged_scores = sorted([scores[idx] for idx in interesting_books_in_lib])[::-1][
        :max_books
    ]
    points_makeable = sum(logged_scores)
    needed_for_non_idle = points_makeable * quantile
    idle_books = max_books - len(logged_scores)
    for idle_books in range(max_books - len(logged_scores), max_books):
        if sum(logged_scores[: max_books - idle_books - 1]) < needed_for_non_idle:
            break
    return nbr_books_processable, points_makeable, idle_books / lib["m"]


def get_lib_to_output(lib, days_left: int, books_to_scan_left: set, scores: list):
    days_left -= lib["t"]
    max_books = max(0, days_left * lib["m"])
    interesting_books_in_lib = lib["ids"] & books_to_scan_left
    logged_books = sorted(interesting_books_in_lib, key=lambda idx: -scores[idx])[
        :max_books
    ]
    books_to_scan_left -= set(logged_books)
    return {"index": lib["index"], "ids": logged_books}


cache = {}


def main(
    ds_name="a_example",
    tparam=1.0,
    mode="div_points",
    pick_rand_topn=1,
    threshold_idle_time=np.inf,
    idle_quantile=0.99,
):
    if ds_name in cache:
        if mode in cache[ds_name]:
            if tparam in cache[ds_name][mode]:
                return cache[ds_name][mode][tparam]
    data = load(ds_name)
    num_books_added_by_last_lib = 1

    books_left = set(range(len(data["S"])))
    unused_libs = list(data["libs"])
    output = []
    days_left = data["D"]
    scores = data["S"]
    est_score = 0
    if mode == "div_points":

        def lib_score(lib):
            nbr_books, nbr_points, idle_time = compute_nbr_books_processable_nbr_points_makeable_idle_time(
                lib,
                days_left=days_left,
                books_to_scan_left=books_left,
                scores=scores,
                quantile=idle_quantile,
            )
            return (idle_time < threshold_idle_time, nbr_points / lib["t"] ** tparam)

    elif mode == "sub_points":

        def lib_score(lib):
            nbr_books, nbr_points, idle_time = compute_nbr_books_processable_nbr_points_makeable_idle_time(
                lib,
                days_left=days_left,
                books_to_scan_left=books_left,
                scores=scores,
                quantile=idle_quantile,
            )
            return (idle_time < threshold_idle_time, nbr_points - lib["t"] * tparam)

    elif mode == "div_books":

        def lib_score(lib):
            nbr_books, nbr_points, idle_time = compute_nbr_books_processable_nbr_points_makeable_idle_time(
                lib,
                days_left=days_left,
                books_to_scan_left=books_left,
                scores=scores,
                quantile=idle_quantile,
            )
            return (idle_time < threshold_idle_time, nbr_books / lib["t"] ** tparam)

    else:
        assert mode == "sub_books"

        def lib_score(lib):
            nbr_books, nbr_points, idle_time = compute_nbr_books_processable_nbr_points_makeable_idle_time(
                lib,
                days_left=days_left,
                books_to_scan_left=books_left,
                scores=scores,
                quantile=idle_quantile,
            )
            return (idle_time < threshold_idle_time, nbr_books - lib["t"] * tparam)

    while num_books_added_by_last_lib > 0 and len(unused_libs) > 0 and days_left >= 0:
        print("start next days left", days_left)
        sel_lib = sorted(unused_libs, key=lib_score)[-pick_rand_topn:]
        np.random.shuffle(sel_lib)
        sel_lib = sel_lib[0]
        est_score += compute_nbr_books_processable_nbr_points_makeable_idle_time(
            sel_lib,
            days_left=days_left,
            books_to_scan_left=books_left,
            scores=scores,
            quantile=idle_quantile,
        )[1]
        if days_left - sel_lib["t"] <= 0:
            break
        del unused_libs[unused_libs.index(sel_lib)]
        output.append(
            get_lib_to_output(
                sel_lib,
                days_left=days_left,
                books_to_scan_left=books_left,
                scores=scores,
            )
        )
        # print("sel_lib", sel_lib)
        days_left -= sel_lib["t"]
        # print("days_left", days_left)
        num_books_added_by_last_lib = len(output[-1]["ids"])
        # print("num_books_added_by_last_lib", num_books_added_by_last_lib)
    print(est_score)
    save(
        output,
        method_name="greedy_best_%s_tparam_%015.7f_pick_top_%d_thresh_idle_%d_quantile_%.3f"
        % (mode, tparam, pick_rand_topn, int(threshold_idle_time), idle_quantile),
        ds_name=ds_name,
    )
    if ds_name not in cache:
        cache[ds_name] = {}
    if mode not in cache[ds_name]:
        cache[ds_name][mode] = {}
    assert tparam not in cache[ds_name][mode]
    cache[ds_name][mode][tparam] = est_score
    return est_score


if __name__ == "__main__":
    import sys

    # modes = sys.argv[1]
    # assert modes in ["div_points", "sub_points", "div_books", "sub_books"]
    from src.solution_super_simple import (
        rel_dsets,
        dset_a,
        dset_b,
        dset_c,
        dset_d,
        dset_e,
        dset_f,
    )
    import numpy as np

    main(
        dset_f,
        tparam=0.55,
        pick_rand_topn=1,
        threshold_idle_time=400.0,
        idle_quantile=0.99,
    )

    # def get_optimal_low_up_by_mode(mode):
    #     if mode == "div_books":
    #         return 1e-2, 1e1
    #     return 1e-9, 1e9

    # for dset in [dset_a, dset_b]:
    #     for mode in [modes]:
    #         low, up = get_optimal_low_up_by_mode(mode)
    #         better_scores_avail = True
    #         while better_scores_avail:
    #             tparams = np.exp(np.linspace(np.log(low), np.log(up), num=4))
    #             results = []
    #             for tparam in tparams:
    #                 results.append(main(dset, mode=mode, tparam=tparam))
    #             argmax = results.index(max(results))
    #             if argmax + 1 < len(results) and results[argmax] == results[argmax + 1]:
    #                 argmax += 1
    #             if argmax == 0:
    #                 argmax += 1
    #             if argmax == len(results) - 1:
    #                 argmax -= 1
    #             assert argmax > 0 and argmax < len(results) - 1
    #             low = tparams[argmax - 1]
    #             up = tparams[argmax + 1]
    #             better_scores_avail = min(results) < max(results)
    # main()
    # for tparam in np.exp(np.linspace(np.log(0.3), np.log(0.7), num=10)):
    #     main(dset_f, tparam=tparam)
    #     print(tparam)
    # for tparam in np.exp(np.linspace(np.log(1e-9), np.log(1e-6), num=10)):
    #     main(dset_e, tparam=tparam)
    #     print(tparam)
    # for tparam in np.exp(np.linspace(np.log(0.87), np.log(0.97), num=10)):
    #     main(dset_c, tparam=tparam)
    #     print(tparam)
    # for tparam in [0.5 ** (i - 10) for i in range(21)]:
    #     for dset in rel_dsets:
    #         main(dset, tparam=tparam)
    # main(dset_d)
