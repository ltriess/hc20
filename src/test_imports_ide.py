#!/usr/bin/env python3

import os.path as osp

from src.common import readvalues

values = readvalues(osp.join(osp.dirname(__file__), "..", ".gitignore"))
print(values[0])
