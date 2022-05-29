# -*- coding: utf-8 -*-

import csv
import sys

def read_csv(file_name):
    file = open(file_name)
    csvreader = csv.reader(file)
    header = next(csvreader)
    # print(header)
    rows = []
    for row in csvreader:
        rows.append(row)
    print(rows[0])
    file.close()

def main(args):
    try:
        file_name = args[1]
        read_csv(file_name)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main(sys.argv)