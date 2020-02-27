#!/usr/bin/env python3


import os.path as osp

from common import dsets, load, load_output, save


def construct_empty_output(lib_order, data):
    output = []
    days_left = data["D"]
    for lib in lib_order:
        lib_data = data["libs"][lib["index"]]
        assert lib_data["index"] == lib["index"]
        days_left -= lib_data["t"]
        books_proc = lib_data["m"] * days_left
        output.append({"index": lib["index"], "books_proc": books_proc, "ids": []})
    return output


def books_by_opportunities(book):
    return -book["nbr_opportunities"]


def books_by_points_div_opportunities(book):
    return book["score"] / book["nbr_opportunities"]


def get_books_left_data(cur_alloc, scores, lib_data):
    books_alloc = set()
    for lib in cur_alloc:
        books_alloc |= set(lib["ids"])
    books_left = {}
    sum_empty_slots = 0
    for lib in cur_alloc:
        assert len(lib["ids"]) <= lib["books_proc"]
        cur_lib_data = lib_data[lib["index"]]
        assert lib["index"] == cur_lib_data["index"]
        assert lib["books_proc"] > 0
        nbr_empty_slots = lib["books_proc"] - len(lib["ids"])
        if nbr_empty_slots == 0:
            continue
        sum_empty_slots += nbr_empty_slots
        best_points = sum(
            sorted([scores[id] for id in cur_lib_data["ids"] if id not in books_alloc])[
                ::-1
            ][:nbr_empty_slots]
        )
        lib_score_for_book_placement = -best_points / nbr_empty_slots
        for book_id in cur_lib_data["ids"]:
            if book_id in books_alloc:
                continue
            if book_id not in books_left:
                books_left[book_id] = {
                    "id": book_id,
                    "score": scores[book_id],
                    "nbr_opportunities": 1,
                    "put_lib_idx": lib["index"],
                    "put_lib_score": lib_score_for_book_placement,
                }
            else:
                books_left[book_id]["nbr_opportunities"] += 1
                if books_left[book_id]["put_lib_score"] < lib_score_for_book_placement:
                    books_left[book_id]["put_lib_score"] = lib_score_for_book_placement
                    books_left[book_id]["put_lib_idx"] = lib["index"]
    return books_left.values(), sum_empty_slots


def main(output_name, mode="points_div_opportunities", pick_rand_topn=1):
    for ds_name in dsets:
        if ds_name in output_name:
            break
    assert ds_name in output_name
    rest_name = osp.basename(output_name)[len(ds_name) + 1 : -len(".out")]
    data = load(ds_name)
    prev_output = load_output(output_name)
    output = construct_empty_output(prev_output, data)
    lib_id_to_output_id = dict(zip([d["index"] for d in output], range(len(output))))

    if mode == "points_div_opportunities":
        book_score_func = books_by_points_div_opportunities
    else:
        assert mode == "opportunities"
        book_score_func = books_by_opportunities

    est_score = 0
    # books_left_data = init_books_left_data(
    #     output, scores=data["S"], lib_data=data["libs"]
    # )
    while True:
        books_left_data, nbr_empty_slots = get_books_left_data(
            output, data["S"], data["libs"]
        )
        print(nbr_empty_slots, len(books_left_data))
        if books_left_data is None or len(books_left_data) == 0:
            break
        sel_books = sorted(books_left_data, key=book_score_func)[-pick_rand_topn:]
        np.random.shuffle(sel_books)
        sel_book = sel_books[0]
        est_score += data["S"][sel_book["id"]]
        output[lib_id_to_output_id[sel_book["put_lib_idx"]]]["ids"].append(
            sel_book["id"]
        )
    print(est_score)
    save(
        output,
        method_name="greedy_best_books_%s_pick_top_%d_from_%s"
        % (mode, pick_rand_topn, rest_name),
        ds_name=ds_name,
    )
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
    from glob import glob

    main(
        "c_incunabula_000005690378_greedy_best_div_points_tparam_0000001.0000000_pick_top_2_203719.out",
        # mode="opportunities",
        pick_rand_topn=1,
    )
    # files = glob(osp.join(osp.dirname(__file__), "..", "out", dset_b + "*"))
    # files = [osp.basename(f) for f in files if "greedy_best_books_" not in f]
    # for f in files:
    #     main(f, pick_rand_topn=1)
