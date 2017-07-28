"""Encodes a json representation of the business's hours into the 5-bit binary
representation used by the merge business hours turing machine. It takes input
from stdin and outputs the initial tape."""
import json
import sys


def encode_hours(hours):
    result = ''
    for (begin, end) in hours:
        result += encode_in_5_bits(begin)
        result += encode_in_5_bits(end)

    return result


def encode_in_5_bits(number):
    encoded = '{:b}'.format(number)
    assert len(encoded) <= 5

    # Add leading zeros
    return '0' * (5 - len(encoded)) + encoded


if __name__ == '__main__':
    print(encode_hours(json.load(sys.stdin)))
