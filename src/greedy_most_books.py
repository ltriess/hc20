#!/usr/bin/env python3


from common import load, save


def compute_nbr_books_processable(lib, days_left: int, books_to_scan_left: set):
    days_left -= lib["t"]
    max_books = max(days_left * lib["m"], 0)
    interesting_books_in_lib = lib["ids"] & books_to_scan_left
    result = min(max_books, len(interesting_books_in_lib))
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


def main(ds_name="a_example"):
    data = load(ds_name)
    num_books_added_by_last_lib = 1

    books_left = set(range(len(data["S"])))
    unused_libs = list(data["libs"])
    output = []
    days_left = data["D"]
    scores = data["S"]
    while num_books_added_by_last_lib > 0 and len(unused_libs) > 0 and days_left >= 0:
        print("start next days left", days_left)
        sel_lib = max(
            unused_libs,
            key=lambda lib: compute_nbr_books_processable(
                lib, days_left=days_left, books_to_scan_left=books_left
            ),
        )
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
        print("sel_lib", sel_lib)
        days_left -= sel_lib["t"]
        print("days_left", days_left)
        num_books_added_by_last_lib = len(output[-1]["ids"])
        print("num_books_added_by_last_lib", num_books_added_by_last_lib)
    save(output, method_name="greedy_most_books", ds_name=ds_name)


if __name__ == "__main__":
    from src.solution_super_simple import dsets

    # main()
    for dset in dsets:
        main(dset)
