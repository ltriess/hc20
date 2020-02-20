#!/usr/bin/env python3
import numpy as np
import tqdm
from src.common import load, load_output, save, score


def solution_christoph(data_input):

    # for score
    indices = np.argsort(np.asarray(data_input["S"]))
    indices = indices[::-1]
    sorted_book_indices = np.arange(len(data_input["S"]))[indices]

    libs = data_input["libs"]
    libs_d = dict(enumerate(data_input["libs"]))
    # index -> # book_indices
    arr = {}
    already_used_days = 0

    S = data_input["S"]

    for lib in libs_d.values():
        score = 0
        for book_id in lib['ids']:
            score += S[book_id]
        lib['total_score'] = score
    # sorted([x['total_score'] for x in libs_d.values()], reverse=True)

    D = data_input["D"]

    for book_index in tqdm.tqdm(sorted_book_indices):
        # check which libs contain this book
        valid_libs = []
        for lib in libs:
            if book_index in lib["ids"]:
                valid_libs.append(lib)

        if not valid_libs:
            continue

        # choose lib
        valid_libs_indices = set([x["index"] for x in valid_libs])

        valid_and_listed = valid_libs_indices.intersection(arr.keys())
        valid_and_not_listed = valid_libs_indices - valid_and_listed

        assert valid_and_listed or valid_and_not_listed

        added = False
        valid_listed_sorted_by_t = sorted(
            [libs_d[i] for i in valid_and_listed], key=lambda x: x["t"]
        )
        left = D

        # if len(valid_listed_sorted_by_t) > 10:
        #     print('x')

        arr_sorted_by_t = [(x, libs_d[x]['t']) for x in arr.keys()]
        arr_sorted_by_t = sorted(arr_sorted_by_t, key=lambda x: x[1])

        for vl in arr_sorted_by_t:

            if vl[0] not in valid_and_listed:
                left -= vl[1]
                continue

            vl = libs_d[vl[0]]

            fit = len(arr[vl["index"]]) % vl["m"] == 0
            count_book_time = len(arr[vl["index"]]) // vl["m"]
            if not fit:
                ## use this library as it will not take a day longer -> still fits
                arr[vl["index"]].add(int(book_index))
                added = True
                break

            startup_time = vl["t"]
            if count_book_time + 1 + startup_time < left:
                # still fits, use this
                arr[vl["index"]].add(int(book_index))
                added = True
                break

            # will not fit with one book more, try next of the availables
            left -= startup_time

        if added:
            continue

        if not valid_and_not_listed:
            continue

        # not added soo far !
        valid_unlisted_sorted_by_t = sorted(
            [libs_d[i] for i in valid_and_not_listed], key=lambda x: x["t"]
        )

        smallest_t_lib = valid_unlisted_sorted_by_t[0]

        if smallest_t_lib["t"] < D - already_used_days:
            arr[smallest_t_lib["index"]] = {int(book_index)}
            already_used_days += smallest_t_lib["t"]
        # else:
        #     print("Not adding book {}".format(book_index))

    output = [{"ids": v, "index": k} for k, v in arr.items()]
    return sorted(output, key=lambda x: libs_d[x['index']]['t'])


dset_a = "a_example"
dset_b = "b_read_on"
dset_c = "c_incunabula"
dset_d = "d_tough_choices"
dset_e = "e_so_many_books"
dset_f = "f_libraries_of_the_world"
dsets = [dset_a, dset_b, dset_c, dset_d, dset_e, dset_f]

if __name__ == "__main__":

    dsets = dsets[5:6]
    # dsets = dsets[0:1]
    total_score = 0

    for dset in dsets:
        data_input = load(dset)
        # print(data_input)
        solution_output = solution_christoph(data_input=data_input)
        score_value, filename = save(
            solution_output, method_name="method", ds_name=dset
        )
        print(dset)
        print(score(solution_output, data_input))

        total_score += score_value

        # solution_output = load_output(filename)
        # print(solution_output)

    print("total")
    print(total_score)
