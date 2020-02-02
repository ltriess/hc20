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

    for i, row in enumerate(matrix):
        free = np.sum(row)
        broken = row.shape[0] - free

        slots = 1
        prev = True
        for j, col in enumerate(row):
            if col:
                prev = True
            else:
                if 0 < j < row.shape[0] - 1 and prev:
                    slots += 1
                prev = False

        size_slots = [0] * slots
        slot = 0
        prev = True
        for j, col in enumerate(row):
            if col:
                size_slots[slot] += 1
                prev = True
            else:
                if 0 < j < row.shape[0] - 1 and prev:
                    slot += 1
                prev = False

        print("Row {}: free: {}, broken: {}, consecutive slots: {}, slot sizes: {}".format(
            i, free, broken, slots, size_slots
        ))

    print("{:.2f}% of slots are available".format(
        100 * np.sum(matrix) / (s[0] * s[1])))

    plt.imshow(matrix)
    plt.show()


def total_server_size_over_matrix_size(matrix, servers):
    available_slots = np.sum(matrix)
    server_slots = sum([server["size"] for server in servers])

    print("There are {} server slots and {} available slots".format(
        server_slots, available_slots
    ))

    return server_slots, available_slots


def order_servers(servers):
    s_cs = []
    for server in servers:
        s_cs.append(server["capacity"] / server["size"])

    inds = np.argsort(s_cs)
    return list(np.array(servers)[inds])[::-1]


def simplified_capa(servers):
    capa = []
    for server in servers:
        for _ in range(server["size"]):
            capa.append(server["capacity"] / server["size"])

    return capa


def max_possible_capa(matrix, servers):
    capa = simplified_capa(order_servers(servers))
    _, available_slots = total_server_size_over_matrix_size(matrix, servers)

    print("The maximum sum of capacity if severs are distributed in available "
          "slots without any constrains".format(sum(capa[:available_slots])))


def main():
    unavailable, servers, pools = load(example=False)

    size_vs_capacity(servers)
    matrix_stats(unavailable)
    max_possible_capa(unavailable, servers)


if __name__ == "__main__":
    main()
