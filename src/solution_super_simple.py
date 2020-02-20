#!/usr/bin/env python3

from src.common import load, load_output, save, score
from src.common import load, save, score, load_output
import numpy as np

def solution_super_simple(data_input):
    print(data_input)
    books_left = []
    for lib in data_input["libs"]:
        books_left += list(lib["ids"])

    books_left = set(books_left)

    days_left = data_input["D"]
    libs_left = [lib['index'] for lib in data_input['libs']]
    output = []
    while days_left > 0 and len(libs_left) > 0:
        possible_lib_scores = []
        # find lib scores
        for lib_id in libs_left:
            lib = [lib for lib in data_input['libs'] if lib['index'] == lib_id][0]
            books_left_at_lib = books_left & lib["ids"]
            scores_of_books_left_at_lib = [
                data_input["S"][book_id] for book_id in books_left_at_lib
            ]
            ids_of_books_left_at_lib = [book_id for book_id in books_left_at_lib]

            scores_of_books_left_at_lib, ids_of_books_left_at_lib = zip(
                *sorted(zip(scores_of_books_left_at_lib, ids_of_books_left_at_lib))
            )

            time_to_scan = days_left // lib["m"]
            max_lib_score = 0
            for book_score, book_id in zip(
                scores_of_books_left_at_lib[:time_to_scan],
                ids_of_books_left_at_lib[:time_to_scan],
            ):
                max_lib_score += book_score

            possible_lib_scores.append(max_lib_score)

        # choose best lib
        max_lib_idx = np.argmax(possible_lib_scores)
        chosen_lib = [lib for lib in data_input['libs'] if lib['index'] == max_lib_idx][0]

        books_left_at_lib = books_left & chosen_lib["ids"]
        scores_of_books_left_at_lib = [
            data_input["S"][book_id] for book_id in books_left_at_lib
        ]
        ids_of_books_left_at_lib = [book_id for book_id in books_left_at_lib]

        scores_of_books_left_at_lib, ids_of_books_left_at_lib = zip(
            *sorted(zip(scores_of_books_left_at_lib, ids_of_books_left_at_lib))
        )
        time_to_scan = days_left // chosen_lib["m"]

        book_ids_taken = []
        for book_score, book_id in zip(
                scores_of_books_left_at_lib[:time_to_scan],
                ids_of_books_left_at_lib[:time_to_scan],
        ):
            book_ids_taken.append(book_id)
        book_ids_taken = set(book_ids_taken)

        books_left -= book_ids_taken
        libs_left = [id for id in libs_left if id != max_lib_idx]
        days_left -= chosen_lib['t']
        entry = {}
        entry['ids'] = book_ids_taken
        entry['index'] = chosen_lib['index']
        output.append(entry)

    return {'libs': output}


dset_a = "a_example"
dset_b = "b_read_on"
dset_c = "c_incunabula"
dset_d = "d_tough_choices"
dset_e = "e_so_many_books"
dset_f = "f_libraries_of_the_world"
dsets = [dset_a, dset_b, dset_c, dset_d, dset_e, dset_f]
rel_dsets = [dset_c, dset_e, dset_f]

if __name__ == "__main__":

    # dsets = dsets[0:1]

    total_score = 0

    for dset in dsets:
        data_input = load(dset)
        print(data_input)
        solution_output = solution_super_simple(data_input=data_input)
        score_value, filename = save(
            solution_output, method_name="method", ds_name=dset
        )
        print(score(solution_output, data_input))

        total_score += score_value

        # solution_output = load_output(filename)
        # print(solution_output)

    print(total_score)
