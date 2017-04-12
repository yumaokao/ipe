#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fileencoding=UTF-8:ts=4:sw=4:sta:et:sts=4:ai

import re
import csv

def main():
    with open('output_105419.csv', newline='') as f:
        reader = csv.reader(f)
        rows = [r for r in reader]
        print(len(rows))

        '''
        for r in reader:
            if 'decode' in r[1]:
                print("{}, {}, {}, {}, {}".format(*r))
        '''


if __name__ == "__main__":
    main()
