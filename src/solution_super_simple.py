#!/usr/bin/env python3

from src.common import load, load_output, save, score


def solution_super_simple(data_input):
    return {"libs": []}


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
