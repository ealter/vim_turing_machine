"""Decodes a binary string to a json representation of the intervals
after the merge overlapping intervals turing machine have processed them. Reads
json from the command line and outputs the initial tape."""
import json
import sys

from vim_turing_machine.constants import BITS_PER_NUMBER
from vim_turing_machine.constants import BLANK_CHARACTER


def decode_intervals(intervals, num_bits=BITS_PER_NUMBER):
    result = []
    clean_intervals = intervals.replace(BLANK_CHARACTER, '').replace(' ', '')
    index = 0
    while index < len(clean_intervals):
        begin = clean_intervals[index:index + num_bits]
        begin = int(begin, 2)
        index += num_bits
        end = clean_intervals[index:index + num_bits]
        end = int(end, 2)
        index += num_bits
        result.append([begin, end])

    return result


if __name__ == '__main__':
    print(json.dumps(decode_intervals(sys.argv[1], int(sys.argv[2]))))
