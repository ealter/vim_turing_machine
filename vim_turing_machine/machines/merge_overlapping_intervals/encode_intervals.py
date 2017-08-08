"""Encodes a json representation of the intervals into the 5-bit binary
representation used by the merge overlapping intervals turing machine. It
takes input from stdin and outputs the initial tape."""
import json
import sys

from vim_turing_machine.constants import BITS_PER_NUMBER


def encode_intervals(intervals, num_bits=BITS_PER_NUMBER):
    result = ''
    for (begin, end) in intervals:
        result += encode_in_x_bits(begin, num_bits)
        result += encode_in_x_bits(end, num_bits)

    return result


def encode_in_x_bits(number, num_bits):
    encoded = '{:b}'.format(number)
    assert len(encoded) <= num_bits

    # Add leading zeros
    return '0' * (num_bits - len(encoded)) + encoded


if __name__ == '__main__':
    print(encode_intervals(json.load(sys.stdin)))
