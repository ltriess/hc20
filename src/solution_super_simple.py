#!/usr/bin/env python3

from src.common import load, save, score, load_output


def solution_super_simple(data_input):
    return {}


if __name__ == "__main__":
    dset = "example"

    data_input = load(dset)
    print(data_input)
    solution_output = solution_super_simple(data_input=data_input)
    score_value, filename = save(solution_output, method_name="method", ds_name=dset)
    print(score(solution_output, data_input))
    solution_output = load_output(filename)
    print(solution_output)
