#!/usr/bin/env python3

from src.common import load
import numpy as np


def analyse(data_input):

    num_books_ids = data_input["B"]
    num_libraries = data_input["L"]
    scanning_time = data_input["D"]
    scores = data_input["S"]

    print("Book ids:", num_books_ids, "Num libs", num_libraries, "Days for scanning:", scanning_time)
    print("Total Scores", sum(scores), "Min", min(scores), "Max", max(scores), "Mean", np.mean(scores))

    all_books = set()

    # for each library
    lib_scores = []
    lib_books = []
    lib_sign_ups = []
    lib_shipping = []
    for library in data_input["libs"]:
        index = library["index"]
        num_books = library["n"]
        sign_up = library["t"]
        shipping_per_day = library["m"]
        book_ids = library["ids"]

        lib_books.append(num_books)
        lib_sign_ups.append(sign_up)
        lib_shipping.append(shipping_per_day)

        all_books.update(book_ids)

        s = [scores[idx] for idx in book_ids]
        lib_scores.extend(s)

    print("Sign Up: Min", min(lib_sign_ups), "Max", max(lib_sign_ups), "Mean", np.mean(lib_sign_ups))
    print("Num Books:", "Total", sum(lib_books), "Min", min(lib_books), "Max", max(lib_books), "Mean", np.mean(lib_books))
    print("Shipping Time:", "Min", min(lib_shipping), "Max", max(lib_shipping), "Mean", np.mean(lib_shipping))

    # Nice, all books in at least one library
    assert len(all_books) <= num_books_ids

    # Get upper bound
    most_valueable_books = []
    for library in data_input["libs"]:
        index = library["index"]
        num_books = library["n"]
        sign_up = library["t"]
        shipping_per_day = library["m"]
        book_ids = library["ids"]

        max_books = (scanning_time - sign_up) * shipping_per_day

        counter = 0
        for b in book_ids:
            if b not in most_valueable_books:
                most_valueable_books.append(b)
                counter += 1
            if counter == max_books:
                break

    upper_bound = sum([scores[idx] for idx in most_valueable_books])
    print("Upper Bound:", upper_bound)


if __name__ == "__main__":

    debug = False

    if debug:
        analyse(load("a_example"))
    else:
        datasets = ["a_example", "b_read_on", "c_incunabula", "d_tough_choices", "e_so_many_books", "f_libraries_of_the_world"]

        for dataset in datasets:
            print("#################################")
            print(dataset)
            analyse(data_input=load(dataset))
