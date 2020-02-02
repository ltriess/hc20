#!/usr/bin/env python3

import matplotlib.pyplot as plt

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


def main():
    unavailable, servers, pools = load(example=False)

    print(unavailable)
    print(servers)
    print(pools)

    # size_vs_capacity(servers)
    get_num_rows_slots(unavailable)


if __name__ == "__main__":
    main()
