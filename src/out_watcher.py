#!/usr/bin/env python3

import os
import os.path as osp
import subprocess
from glob import glob
from shutil import copy2 as copy
from time import sleep

from src.common import dsets, get_time_stamp


def num_with_underscores(score):
    score = str(score)
    if "." in score:
        i, f = score.split(".")
        und_f = ""
        while len(f) >= 4:
            und_f += f[:3]
            und_f += "_"
            f = f[3:]
        und_f += f
    else:
        i = score
    i = i[::-1]
    und_i = ""
    while len(i) >= 4:
        und_i += i[:3]
        und_i += "_"
        i = i[3:]
    und_i += i
    und_i = und_i[::-1]
    if "." in score:
        return und_i + "." + und_f
    else:
        return und_i


def zip_src():
    subprocess.check_output(
        "./zipall.bash", shell=True, cwd=osp.join(osp.dirname(__file__), "..")
    )


def copy_out_to_best(fname_high_score):
    target_best_out_fname = osp.join(
        osp.dirname(__file__), "..", "best_out", osp.basename(fname_high_score)
    )
    if not osp.exists(target_best_out_fname):
        copy(fname_high_score, target_best_out_fname)
        zip_src()


def get_best_scores(filename):
    with open(filename, "r") as fin:
        lines = fin.readlines()
    best_scores = {}
    for line in lines[1:]:
        dset, score, username = line.strip().split()
        score = int(score)
        best_scores[dset] = {"score": score, "username": username}
    return best_scores


def write_best_scores(filename, best_scores):
    maxlen_dsets = max(map(len, dsets))
    maxlen_usernames = max(map(len, [best_scores[dset]["username"] for dset in dsets]))
    total_score = sum(best_scores[dset]["score"] for dset in dsets)
    max_len_scores = max(
        map(
            lambda s: len(num_with_underscores(s)),
            [best_scores[dset]["score"] for dset in dsets],
        )
    )
    with open(filename, "w") as fout:
        fout.write(num_with_underscores(total_score))
        fout.write("\n")
        for dset in dsets:
            fout.write(
                (
                    "%"
                    + str(maxlen_dsets)
                    + "s %"
                    + str(max_len_scores)
                    + "s %"
                    + str(maxlen_usernames)
                    + "s"
                )
                % (
                    dset,
                    num_with_underscores(best_scores[dset]["score"]),
                    best_scores[dset]["username"],
                )
            )
            fout.write("\n")


if __name__ == "__main__":
    username = os.getenv("USER")
    best_scores = {dset: {"username": "None", "score": 0} for dset in dsets}
    best_scores_filename = osp.join(osp.dirname(__file__), "..", "best_scores.out")
    if osp.exists(best_scores_filename):
        best_scores = get_best_scores(best_scores_filename)
    old_score = 0

    while True:
        score = 0
        for dset in dsets:
            fname_high_score = sorted(
                glob(osp.join(osp.dirname(__file__), "..", "out", "%s*.out" % dset))
            )[-1]
            score = int(osp.basename(fname_high_score)[len(dset) + 1 :].split("_")[0])
            if score > best_scores[dset]["score"]:
                best_scores[dset] = {"score": score, "username": username}
                copy_out_to_best(fname_high_score)
                write_best_scores(best_scores_filename, best_scores)
        score = sum(best_scores[dset]["score"] for dset in dsets)
        if score > old_score:
            print(
                get_time_stamp(with_date=False, with_delims=True),
                num_with_underscores(score),
            )
            old_score = score
        sleep(10)
