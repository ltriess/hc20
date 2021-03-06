#!/usr/bin/env python3

import os.path as osp
import time

import numpy as np

dset_a = "a_example"
dset_b = "b_read_on"
dset_c = "c_incunabula"
dset_d = "d_tough_choices"
dset_e = "e_so_many_books"
dset_f = "f_libraries_of_the_world"
dsets = [dset_a, dset_b, dset_c, dset_d, dset_e, dset_f]
rel_dsets = [dset_c, dset_e, dset_f]


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
    filename = osp.join(osp.dirname(__file__), "..", "in", ds_name + ".txt")
    values = readvalues(filename)
    data = {}
    # Todo unpack values into structured dict data

    data["B"] = values[0][0]
    data["L"] = values[0][1]
    data["D"] = values[0][2]

    data["S"] = np.asarray(values[1])

    data["ids"] = []

    data["N"] = []
    data["T"] = []
    data["M"] = []

    for l in range(data["L"]):
        n, t, m = values[2 * l + 2]
        data["ids"].append(values[2 * l + 2 + 1])
        data["N"].append(n)
        data["T"].append(t)
        data["M"].append(m)

    data["libs"] = [
        {
            "index": i,
            "n": data["N"][i],
            "t": data["T"][i],
            "m": data["M"][i],
            "ids": set(data["ids"][i]),
        }
        for i in range(data["L"])
    ]

    del data["ids"]
    del data["N"]
    del data["T"]
    del data["M"]

    return data


def save(output, method_name="example", ds_name="example"):
    data = load(ds_name)
    s = score(output, data)
    outfilename = osp.join(
        osp.dirname(__file__),
        "..",
        "out",
        "%s_%012d_%s_%s.out"
        % (ds_name, s, method_name, get_time_stamp(with_date=False, with_delims=False)),
    )

    try:
        output = output["libs"]
    except:
        pass

    # Todo pack output dict into list of lists of values (corresponding to rows)
    output_lists = []
    output_lists.append([len(output)])

    for lib in output:
        book_ids = lib["ids"]
        assert bool(book_ids)
        output_lists.append([lib["index"], len(book_ids)])
        output_lists.append(list(book_ids))

    writevalues(output_lists, outfilename)
    return s, outfilename


def load_output(filename):
    filepath = osp.join(osp.dirname(__file__), "..", "out", filename)
    values = readvalues(filepath)
    # Todo unpack list of list of values into output dict
    n = values[0][0]
    values = values[1:]
    assert len(values) == 2 * n
    output = []
    for i in range(n):
        lib_id, num_books = values[2 * i]
        assert len(values[2 * i + 1]) == num_books
        ids = values[2 * i + 1]
        output.append({"index": lib_id, "ids": ids})
    return output


def score(output, data):
    # check if output is valid else raise assertion
    # Todo then compute score and return it

    # do not allow duplicate books!
    all_books = set()

    try:
        output = output["libs"]
    except:
        pass

    for lib in output:
        if all_books.intersection(lib["ids"]):
            raise RuntimeError(
                "Duplicate books in output. {}".format(
                    all_books.intersection(lib["ids"])
                )
            )
        all_books = all_books.union(lib["ids"])

    score = 0

    day_start = 0
    for lib in output:
        i = lib["index"]
        l = data["libs"][i]
        assert l["index"] == i
        day_start += l["t"]

        if len(lib["ids"]) % l["m"] == 0:
            days_necessary = len(lib["ids"]) // l["m"]
        else:
            days_necessary = len(lib["ids"]) // l["m"] + 1

        if days_necessary > data["D"] - day_start:
            raise RuntimeError(
                "too many books in library {}!. Signup finished"
                "in day {}. Books in libarary: {}. Days necessary: {}. Days left: {}".format(
                    lib["index"],
                    day_start,
                    len(lib["ids"]),
                    days_necessary,
                    data["D"] - day_start,
                )
            )

        for book_id in lib["ids"]:
            score += data["S"][book_id]

    return score


if __name__ == "__main__":
    example_input = load("example")
    print(example_input)
    example_output = {}
    score_value, filename = save(
        example_output, method_name="method", ds_name="example"
    )
    print(score(example_output, example_input))
    example_output = load_output(filename)
    print(example_output)
