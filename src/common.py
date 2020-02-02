#!/usr/bin/env python3

import os.path as osp
import time

import numpy as np
import pathlib


def get_time_stamp(with_date=True, with_delims=False):
    if with_date:
        if with_delims:
            return time.strftime("%Y/%m/%d-%H:%M:%S")
        else:
            return time.strftime("%Y%m%d-%H%M%S")
    else:
        if with_delims:
            return time.strftime("%H:%M:%S")
        else:
            return time.strftime("%H%M%S")


def load(example=True):
    filename = str(pathlib.Path(__file__).parent.parent / 'in' / 'dc.in')
    if example:
        filename = str(pathlib.Path(__file__).parent.parent / 'in' / 'example.in')
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


def save(server_allocation, output_name="example"):
    m = len(server_allocation)
    assert m >= 1
    assert sorted(server_allocation[0].keys()) == ["left_slot", "pool_id", "row"]
    outfilename = osp.join(
        osp.dirname(__file__),
        "..",
        "out",
        "%s_%s.out" % (output_name, get_time_stamp(with_date=False, with_delims=False)),
    )
    key_output_order = ["row", "left_slot", "pool_id"]
    with open(outfilename, "w") as fout:
        for alloc in server_allocation:
            if alloc["left_slot"] == -1:
                assert alloc["pool_id"] == -1
                assert alloc["row"] == -1
                fout.write("x\n")
            else:
                fout.write("%s\n" % " ".join([str(alloc[k]) for k in key_output_order]))


if __name__ == "__main__":
    print(load(example=True))
    save(
        [
            {"left_slot": -1, "pool_id": -1, "row": -1},
            {"left_slot": 3, "pool_id": 0, "row": 2},
        ],
        output_name="test",
    )
