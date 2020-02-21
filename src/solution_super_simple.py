#!/usr/bin/env python3
#!/usr/bin/env python3

import os.path as osp
import time
import numpy as np


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
        "%s_%s_%012d_%s.out"
        % (ds_name, method_name, s, get_time_stamp(with_date=False, with_delims=False)),
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
        # assert bool(book_ids)
        output_lists.append([lib["index"], len(book_ids)])
        output_lists.append(list(book_ids))

    writevalues(output_lists, outfilename)
    return s, outfilename


def load_output(filename):
    filepath = osp.join(osp.dirname(__file__), "..", "out", filename)
    values = readvalues(filepath)
    # Todo unpack list of list of values into output dict
    output = {}
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


def solution_super_simple(data_input):
    books_left = []
    for lib in data_input["libs"]:
        books_left += list(lib["ids"])

    books_left = set(books_left)

    days_left = data_input["D"]
    libs_left = [lib["index"] for lib in data_input["libs"]]
    output = []

    num_retries = 10000
    while days_left > 0 and len(libs_left) > 0 and num_retries > 0:
        print("Days left {}".format(days_left))
        possible_lib_scores = []
        # find lib scores
        for lib_id in libs_left:
            lib = [lib for lib in data_input["libs"] if lib["index"] == lib_id][0]
            books_left_at_lib = books_left & lib["ids"]
            scores_of_books_left_at_lib = [
                data_input["S"][book_id] for book_id in books_left_at_lib
            ]
            ids_of_books_left_at_lib = list(books_left_at_lib)
            if len(ids_of_books_left_at_lib) == 0:
                continue
            scores_of_books_left_at_lib, ids_of_books_left_at_lib = zip(
                *sorted(zip(scores_of_books_left_at_lib, ids_of_books_left_at_lib))
            )

            max_num_books_to_scan = days_left * lib["m"]
            max_lib_score = 0
            for book_score, book_id in zip(
                scores_of_books_left_at_lib[:max_num_books_to_scan],
                ids_of_books_left_at_lib[:max_num_books_to_scan],
            ):
                max_lib_score += book_score

            possible_lib_scores.append(max_lib_score**2/np.sqrt(lib["t"]))

        # choose best lib
        max_lib_idx = int(np.argmax(possible_lib_scores))
        max_lib_idx = libs_left[max_lib_idx]
        chosen_lib = [lib for lib in data_input["libs"] if lib["index"] == max_lib_idx][
            0
        ]

        books_left_at_lib = books_left & chosen_lib["ids"]
        scores_of_books_left_at_lib = [
            data_input["S"][book_id] for book_id in books_left_at_lib
        ]

        ids_of_books_left_at_lib = [book_id for book_id in books_left_at_lib]
        if len(ids_of_books_left_at_lib) == 0:
            num_retries -= 1
            libs_left = [id for id in libs_left if id != max_lib_idx]
            continue
        scores_of_books_left_at_lib, ids_of_books_left_at_lib = zip(
            *sorted(zip(scores_of_books_left_at_lib, ids_of_books_left_at_lib))
        )

        book_ids_taken = []
        days_left_tmp = days_left
        days_left_tmp -= chosen_lib["t"]

        max_num_books_to_scan = days_left * chosen_lib["m"]
        if max_num_books_to_scan < 0:
            num_retries -= 1
            libs_left = [id for id in libs_left if id != max_lib_idx]
            continue
        days_left -= chosen_lib["t"]

        for book_score, book_id in zip(
            scores_of_books_left_at_lib[:max_num_books_to_scan],
            ids_of_books_left_at_lib[:max_num_books_to_scan],
        ):
            book_ids_taken.append(book_id)

        book_ids_taken = set(book_ids_taken)

        books_left -= book_ids_taken
        libs_left = [id for id in libs_left if id != max_lib_idx]
        entry = {}
        entry["ids"] = book_ids_taken
        entry["index"] = chosen_lib["index"]
        output.append(entry)

    return {"libs": output}


import sys


def main():
    dset_a = "a_example"
    dset_b = "b_read_on"
    dset_c = "c_incunabula"
    dset_d = "d_tough_choices"
    dset_e = "e_so_many_books"
    dset_f = "f_libraries_of_the_world"
    dsets = [dset_a, dset_b, dset_c, dset_d, dset_e, dset_f]

    if len(sys.argv) > 1:
        ds_id = int(sys.argv[1])
        dsets = [dsets[ds_id]]

    total_score = 0

    for dset in dsets:
        data_input = load(dset)
        solution_output = solution_super_simple(data_input=data_input)
        score_value, filename = save(
            solution_output, method_name="method", ds_name=dset
        )
        print(score(solution_output, data_input))

        total_score += score_value

        # solution_output = load_output(filename)
        # print(solution_output)

    print(total_score)


if __name__ == "__main__":
    main()

