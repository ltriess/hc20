#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

from src.common import load


def size_vs_capacity(servers):

    x = []
    y = []
    for server in servers:
        size = server["size"]
        capacity = server["capacity"]
        x.append(size)
        y.append(capacity)

    print("Sum capacity: {}".format(sum(y)))
    print("Max capacity: {}, Min capacity: {}".format(max(y), min(y)))
    print("Number of servers: {}".format(len(servers)))

    fig, ax = plt.subplots()
    ax.scatter(x, y)
    ax.grid(True)
    plt.xlabel("Size")
    plt.ylabel("Capacity")
    plt.show()


def matrix_stats(matrix):
    s = matrix.shape

    print("Number of rows {}".format(s[0]))
    print("Number of slots {}".format(s[1]))

    print("{:.2f}% of slots are available".format(
        100 * np.sum(matrix) / (s[0] * s[1])))

    plt.imshow(matrix)
    plt.show()


def order_servers(servers):
    s_cs = []
    for server in servers:
        s_cs.append(server["capacity"] / server["size"])

    inds = np.argsort(s_cs)
    return list(np.array(servers)[inds])[::-1]


def main():
    unavailable, servers, pools = load(example=False)

    print(unavailable)
    print(servers)
    print(pools)

    # size_vs_capacity(servers)
    # matrix_stats(unavailable)


if __name__ == "__main__":
    main()
