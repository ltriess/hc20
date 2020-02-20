#!/usr/bin/env python3

from src.common import load


def analyse(data_input):
    return {}


if __name__ == "__main__":
    dset = "example"

    data_input = load(dset)
    print(data_input)
    solution_output = analyse(data_input=data_input)
