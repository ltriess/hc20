#!/usr/bin/env python3

import numpy as np


def load(example=True):
    filename = "../in/dc.in"
    if example:
        filename = "../in/example.in"
    with open(filename, "r") as fin:
        lines = fin.readlines()
    lines = [line.strip() for line in lines]
    r, s, u, p, m = map(int, lines[0].split(" "))
    lines = lines[1:]
    ulines = lines[:u]
    mlines = lines[u:]
    assert len(mlines) == m
    available = np.ones((r, s), dtype=np.bool)
    for uline in ulines:
        ri, si = map(int, uline.split(" "))
        available[ri, si] = False
    servers = []
    for i, mline in enumerate(mlines):
        zi, ci = map(int, mline.split(" "))
        servers.append({"id": i, "size": zi, "capacity": ci})
    return available, servers, p


if __name__ == "__main__":
    print(load(example=True))
