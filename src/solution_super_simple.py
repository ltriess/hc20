#!/usr/bin/env python3

from src.common import load, save, score, load_output


def solution_super_simple(data_input):
    return {}


if __name__ == "__main__":

    # dset = "example"
    dset_a = "a_example"
    dset_b = "b_small"
    dset_c = "c_medium"
    dset_d = "d_quite_big"
    dset_e = "e_also_big"
    dsets = [dset_a, dset_b, dset_c, dset_d, dset_e]

    dsets = dsets[0:1]

    total_score = 0

    for dset in dsets:
        data_input = load(dset)
        print(data_input)
        solution_output = solution_super_simple(data_input=data_input)
        score_value, filename = save(solution_output, method_name="method", ds_name=dset)
        print(score(solution_output, data_input))

        total_score += score_value

        # solution_output = load_output(filename)
        # print(solution_output)

    print(total_score)