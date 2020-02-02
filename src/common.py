#!/usr/bin/env python3

import os.path as osp
import pathlib
import time

import numpy as np

key_output_order = ["row", "left_slot", "pool_id"]


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
    filename = str(pathlib.Path(__file__).parent / ".." / "in" / "dc.in")
    if example:
        filename = str(pathlib.Path(__file__).parent / ".." / "in" / "example.in")
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


def save(server_allocation, available, servers, nbr_pools, output_name="example"):
    s = score(server_allocation, available, servers, nbr_pools)
    m = len(server_allocation)
    assert m >= 1
    assert sorted(server_allocation[0].keys()) == ["left_slot", "pool_id", "row"]
    outfilename = osp.join(
        osp.dirname(__file__),
        "..",
        "out",
        "%s_%06d_%s.out"
        % (output_name, s, get_time_stamp(with_date=False, with_delims=False)),
    )
    with open(outfilename, "w") as fout:
        for alloc in server_allocation:
            if alloc["left_slot"] == -1:
                fout.write("x\n")
            else:
                fout.write("%s\n" % " ".join([str(alloc[k]) for k in key_output_order]))


def load_output(filename):
    filepath = osp.join(osp.dirname(__file__), "..", "out", filename)
    with open(filepath, "r") as fin:
        lines = fin.readlines()
    lines = [line.strip() for line in lines]
    server_allocation = []
    for line in lines:
        if line == "x":
            line = "-1 -1 -1"
        server_allocation.append(
            dict(zip(key_output_order, list(map(int, line.split(" ")))))
        )
    return server_allocation


def check_if_allocation_fits(server_allocation, available, servers):
    used = np.logical_not(available)
    m = len(server_allocation)
    for i in range(m):
        if server_allocation[i]["row"] == -1:
            assert server_allocation[i]["left_slot"] == -1, "not all values set to -1"
            assert server_allocation[i]["pool_id"] == -1, "not all values set to -1"
            continue
        size = servers[i]["size"]
        start = server_allocation[i]["left_slot"]
        end = start + size
        assert start >= 0, "server placed outside of row length"
        assert end <= available.shape[1], "server placed outside of row length"
        row = server_allocation[i]["row"]
        assert row >= 0, "server placed outside of 0...r-1"
        assert row < used.shape[0], "server placed outside of 0...r-1"
        assert not np.any(used[row, start:end])
        used[row, start:end] = True
    return


def score(server_allocation, available, servers, nbr_pools):
    m = len(servers)
    assert len(server_allocation) == m
    check_if_allocation_fits(server_allocation, available, servers)
    row_capacities = np.zeros([available.shape[0], nbr_pools], dtype=np.int)
    for i in range(m):
        if server_allocation[i]["row"] == -1:
            continue
        row_capacities[
            server_allocation[i]["row"], server_allocation[i]["pool_id"]
        ] += servers[i]["capacity"]
    gc = row_capacities.sum(axis=0) - row_capacities.max(axis=0)
    return gc.min()


if __name__ == "__main__":
    example_input = load(example=True)
    print(example_input)
    save(
        [
            {"left_slot": -1, "pool_id": -1, "row": -1},
            {"left_slot": 1, "pool_id": 0, "row": 0},
            {"left_slot": -1, "pool_id": -1, "row": -1},
            {"left_slot": -1, "pool_id": -1, "row": -1},
            {"left_slot": -1, "pool_id": -1, "row": -1},
        ],
        *example_input,
        output_name="test",
    )
    example_output = load_output("task_example.out")
    print(example_output)
    print(score(example_output, *example_input))
