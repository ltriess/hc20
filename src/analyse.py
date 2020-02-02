#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

from src.common import load


def size_vs_capacity(servers):

    x = []
    y = []
    for server in servers:
        x.append(server["size"])
        y.append(server["capacity"])

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.grid(True)
    plt.xlabel("Size")
    plt.ylabel("Capacity")
    plt.show()


def get_num_rows_slots(matrix):
    s = matrix.shape

    print("Number of rows {}".format(s[0]))
    print("Number of slots {}".format(s[1]))

    return s


def percentage_available_slots(matrix):
    print("{:.2f}% of slots are available".format(
        100 * np.sum(matrix) / (matrix.shape[0] * matrix.shape[1])))


def main():
    unavailable, servers, pools = load(example=False)

    print(unavailable)
    print(servers)
    print(pools)

    # size_vs_capacity(servers)
    # get_num_rows_slots(unavailable)
    # percentage_available_slots(unavailable)


if __name__ == "__main__":
    main()
