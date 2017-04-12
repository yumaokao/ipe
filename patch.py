#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import re
import csv

def decode_u(a):
    # print(b)
    s = eval(a)
    return s

def main():
    with open('pp.csv', newline='') as f:
        reader = csv.reader(f)
        for r in reader:
            if 'decode' in r[1]:
                r[1] = decode_u(r[1])
                print("{}, {}, {}, {}, {}".format(*r))


if __name__ == "__main__":
    main()
