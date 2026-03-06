#!/usr/bin/python3

import argparse
import hashlib

parser = argparse.ArgumentParser()
parser.add_argument('input_str', help="string to be encrypted (md5)")


def enc(string):
    m = hashlib.md5()
    m.update(string.encode())
    return m.hexdigest()


if __name__ == '__main__':
    args = parser.parse_args()
    print(enc(args.input_str.strip()))
