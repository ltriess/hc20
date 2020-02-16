#!/usr/bin/env python3

import os.path as osp
import time


def cast_to_int_float_str(s: str):
    try:
        r = int(s)
        return r
    except ValueError:
        pass
    try:
        r = float(s)
        return r
    except ValueError:
        pass
    return s


def readvalues(filename):
    with open(filename, "r") as fin:
        lines = fin.readlines()
    lines = [line.strip() for line in lines]
    values = []
    for line in lines:
        values.append(list(map(cast_to_int_float_str, line.split(" "))))
    return values


def writevalues(values, filename):
    with open(filename, "w") as fout:
        for value_row in values:
            fout.write(" ".join(map(str, value_row)))
            fout.write("\n")


def get_time_stamp(with_date=True, with_delims=False):
    if with_date:
        if with_delims:
            return time.strftime("%Y/%m/%d-%H:%M:%S")
        else:
            return time.strftime("%Y%m%d-%H%M%S")
    else:
        if with_delims:
            return time.strftime("%H:%M:%S")
        else:
            return time.strftime("%H%M%S")


def load(ds_name):
    filename = osp.join(osp.dirname(__file__), "..", "in", ds_name + ".in")
    values = readvalues(filename)
    data = {}
    # unpack values into structured dict data
    return data


def save(output, method_name="example", ds_name="example"):
    data = load(ds_name)
    s = score(output, data)
    outfilename = osp.join(
        osp.dirname(__file__),
        "..",
        "out",
        "%s_%s_%06d_%s.out"
        % (ds_name, method_name, s, get_time_stamp(with_date=False, with_delims=False)),
    )
    # pack output dict into list of lists of values (corresponding to rows)
    output_lists = []
    writevalues(output_lists, outfilename)
    return s


def load_output(filename):
    filepath = osp.join(osp.dirname(__file__), "..", "out", filename)
    values = readvalues(filepath)
    # unpack list of list of values into output dict
    output = {}
    return output


def score(output, data):
    # check if output is valid else raise assertion
    # then compute score and return it
    score = 0
    return score


if __name__ == "__main__":
    example_input = load("example")
    print(example_input)
    example_output = {}
    save(example_output, output_name="test")
    print(score(example_output, example_input))
    example_output = load_output("task_example.out")
    print(example_output)
