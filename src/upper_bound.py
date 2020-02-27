#!/usr/bin/env python3


from tqdm import tqdm

from common import load, save


def compute_nbr_books_processable(lib, days_left: int, books_to_scan_left: set):
    days_left -= lib["t"]
    max_books = max(days_left * lib["m"], 0)
    interesting_books_in_lib = lib["ids"] & books_to_scan_left
    result = min(max_books, len(interesting_books_in_lib))
    return result


def compute_nbr_points_makeable(
    lib, days_left: int, books_to_scan_left: set, scores: list
):
    days_left -= lib["t"]
    max_books = max(days_left * lib["m"], 0)
    interesting_books_in_lib = lib["ids"] & books_to_scan_left
    logged_books = sorted(interesting_books_in_lib, key=lambda idx: -scores[idx])[
        :max_books
    ]
    result = sum([scores[idx] for idx in logged_books])
    return result


def get_lib_to_output(lib, days_left: int, books_to_scan_left: set, scores: list):
    days_left -= lib["t"]
    max_books = max(0, days_left * lib["m"])
    interesting_books_in_lib = lib["ids"] & books_to_scan_left
    logged_books = sorted(interesting_books_in_lib, key=lambda idx: -scores[idx])[
        :max_books
    ]
    books_to_scan_left -= set(logged_books)
    return {"index": lib["index"], "ids": logged_books}


# def get_points_per_startup_day(lib, days, scores):
#     books = (days - lib["t"]) * lib["m"]
#     points_per_startup_day = np.zeros(days, np.float32)
#     s = sorted([scores[idx] for idx in lib["ids"]])[::-1][:books]
#     for t in range(days):
#         days_left = max(0, min(days - lib["t"], days - t - 1))
#         cur_score = sum(s[: days_left * lib["m"]])
#         points_per_startup_day[t] = cur_score / lib["t"]
#     # print(points_per_startup_day)
#     return points_per_startup_day


def get_points_per_startup_day(lib, days, scores):
    books = (days - lib["t"]) * lib["m"]
    s = sorted([scores[idx] for idx in lib["ids"]])[::-1][:books]
    if len(s) % lib["m"] != 0:
        s += [0.0] * (lib["m"] - (len(s) % lib["m"]))
    s = np.array(s).reshape(-1, lib["m"]).sum(axis=1)
    if len(s) < days:
        s = np.concatenate([s, np.zeros(days - len(s), np.float32)], axis=0)
    return np.concatenate([[0], np.cumsum(s)[:-1]], axis=0)[::-1] / lib["t"]


def main(ds_name="a_example"):
    data = load(ds_name)
    best_points_per_startup_day = np.zeros(data["D"], dtype=np.float32)

    for lib in tqdm(data["libs"]):
        points_per_startup_day = get_points_per_startup_day(lib, data["D"], data["S"])
        best_points_per_startup_day = np.maximum(
            points_per_startup_day, best_points_per_startup_day
        )

    print(ds_name, best_points_per_startup_day.sum())


if __name__ == "__main__":
    import sys

    # modes = sys.argv[1]
    # assert modes in ["div_points", "sub_points", "div_books", "sub_books"]
    from src.solution_super_simple import (
        rel_dsets,
        dsets,
        dset_a,
        dset_b,
        dset_c,
        dset_d,
        dset_e,
        dset_f,
    )
    import numpy as np

    for dset in dsets:
        main(dset)
