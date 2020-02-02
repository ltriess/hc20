#!/usr/bin/env python3

import matplotlib.pyplot as plt
import numpy as np

from src.common import load_output, load
from src.solution_dummy import solution_dummy


def plot_pool_matrix(server_dict):
    pass


def plot_capacity_matrix(server_dict):
    pass


def main():
    available, servers, p = load(example=False)
    server_dict = solution_dummy(available, servers, p)

    plot_capacity_matrix(server_dict)
    plot_pool_matrix(server_dict)


if __name__ == "__main__":
    main()
