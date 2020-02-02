#!/usr/bin/env python3

import pathlib
import numpy as np
from common import load


def solution_dummy(file: str):
    load(file)


if __name__ == '__main__':
    solution_dummy(pathlib.Path(__file__).parent / 'in' / 'example.in')
    # solution_dummy(pathlib.Path(__file__).parent / 'in' / 'dc.in')
