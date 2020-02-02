#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

from src.common import load
from src.solution_dummy import solution_dummy


def plot_pool_matrix(server_dict, matrix):

    matrix = np.int32(matrix)
    for server in server_dict:

        for i in range(server["size"]):
            matrix[server["row"]][server["left_slot"] + i] = server["pool_id"]

    plt.imshow(matrix)
    plt.show()


def plot_capacity_matrix(server_dict, matrix):

    matrix = np.int32(matrix)
    for server in server_dict:

        for i in range(server["size"]):
            matrix[server["row"]][server["left_slot"] + i] = server["capacity"]

    plt.imshow(matrix)
    plt.show()


def main():
    available, servers, p = load(example=False)
    server_dict = solution_dummy(available, servers, p)

    plot_capacity_matrix(server_dict, available)
    plot_pool_matrix(server_dict, available)


if __name__ == "__main__":
    main()
