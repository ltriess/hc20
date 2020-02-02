#!/usr/bin/env python3

from src.common import load


def size_vs_capacity(servers):
    print(servers)

    for server in servers:
        print(server["size"], server["capacity"])


def main():
    unavailable, servers, pools = load()

    size_vs_capacity(servers)


if __name__ == "__main__":
    main()
