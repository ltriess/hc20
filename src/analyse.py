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


def main():
    unavailable, servers, pools = load()

    size_vs_capacity(servers)


if __name__ == "__main__":
    main()
