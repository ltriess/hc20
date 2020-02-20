#!/usr/bin/env python3
import numpy as np
import tqdm
from src.common import load, load_output, save, score


def solution_christoph(data_input):

    # durations = []
    # for lib in data_input['libs']:
    #     duration = lib['t']
    #     duration_for_books = lib['n'] // lib['m']
    #     if lib['n'] // lib['m'] != 0:
    #         duration_for_books += 1
    #     durations.append(duration + duration_for_books)
    #
    # print(durations)
    #
    # libs = sorted(data_input['libs'], key=lambda k: k['t'])
    #
    # day_start = 0
    # day_total = data_input['D']
    #
    # output = []
    # for lib in libs:
    #     day_start += lib['t']
    #     left = day_total - day_start
    #     if left <= 0:
    #         break
    #     truncated = set(list(lib['ids'])[:left * lib['m']])
    #     lib['ids'] = truncated
    #     output.append(lib)

    # index -> lib
    libs = {}

    # for score
    indices = np.argsort(np.asarray(data_input['S']))
    indices = indices[::-1]
    sorted_book_indices = np.arange(len(data_input['S']))[indices]

    libs = data_input['libs']
    libs_d = dict(enumerate(data_input['libs']))
    # index -> # book_indices
    arr = {}

    D = data_input['D']

    for book_index in tqdm.tqdm(sorted_book_indices[:1000]):
        # check which libs contain this book
        valid_libs = []
        for lib in libs:
            if book_index in lib['ids']:
                valid_libs.append(lib)

        if not valid_libs:
            continue

        # choose lib
        valid_libs_indices = set([x['index'] for x in valid_libs])

        valid_and_listed = valid_libs_indices.intersection(arr.keys())
        valid_and_not_listed = valid_libs_indices - valid_and_listed

        added = False
        valid_listed_sorted_by_t = sorted([libs_d[i] for i in valid_and_listed],
                                          key=lambda x: x['t'])
        left = D
        for vl in valid_listed_sorted_by_t:
            fit = len(arr[vl['index']]) % vl['m'] == 0
            count_book_time = len(arr[vl['index']]) // vl['m']
            if not fit:
                ## use this library as it will not take a day longer -> still fits
                arr[vl['index']].add(int(book_index))
                added = True
                break

            startup_time = vl['t']
            if count_book_time + 1 + startup_time < left:
                # still fits, use this
                arr[vl['index']].add(int(book_index))
                added = True
                break

            # will not fit with one book more, try next of the availables
            left -= startup_time

        if added:
            continue

        # not added soo far !
        valid_unlisted_sorted_by_t = sorted([libs_d[i] for i in valid_and_not_listed],
                                             key=lambda x: x['t'])

        smallest_t_lib = valid_unlisted_sorted_by_t[0]

        if smallest_t_lib['t'] < left:
            arr[smallest_t_lib['index']] = {int(book_index)}

    output = [libs_d[k] for k, v in arr.items()]
    return output


dset_a = "a_example"
dset_b = "b_read_on"
dset_c = "c_incunabula"
dset_d = "d_tough_choices"
dset_e = "e_so_many_books"
dset_f = "f_libraries_of_the_world"
dsets = [dset_a, dset_b, dset_c, dset_d, dset_e, dset_f]

if __name__ == "__main__":

    dsets = dsets[2:3]

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
