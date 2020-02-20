#!/usr/bin/env python3

from src.common import load


def analyse(data_input):

    num_books_ids = data_input["B"]
    num_libraries = data_input["L"]
    scanning_time = data_input["D"]

    print("Number of books:", num_books_ids)
    print("Number of libraries:", num_libraries)
    print("Days for scanning:", scanning_time)

    scores = data_input["S"]
    print("Scores:", scores)

    # for each library
    for library in data_input["libs"]:
        index = library["index"]
        num_books = library["n"]
        sign_up = library["t"]
        shipping_per_day = library["m"]

        book_ids = library["ids"]


if __name__ == "__main__":

    datasets = ["a_example", "b_read_on", "c_incunabula", "d_tough_choices", "e_so_many_books", "f_libraries_of_the_world"]

    for dataset in datasets:
        print("#################################")
        print(dataset)
        analyse(data_input=load(dataset))
        print("#################################")
