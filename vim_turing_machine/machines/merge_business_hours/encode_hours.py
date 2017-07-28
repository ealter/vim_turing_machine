"""Encodes a json representation of the business's hours into the 5-bit binary
representation used by the merge business hours turing machine. It takes input
from stdin and outputs the initial tape."""
import json
import sys


def encode_hours(hours, num_bits=5):
    result = ''
    for (begin, end) in hours:
        result += encode_in_x_bits(begin, num_bits)
        result += encode_in_x_bits(end, num_bits)

    return result


def encode_in_x_bits(number, num_bits):
    encoded = '{:b}'.format(number)
    assert len(encoded) <= num_bits

    # Add leading zeros
    return '0' * (num_bits - len(encoded)) + encoded


if __name__ == '__main__':
    print(encode_hours(json.loads(sys.stdin)))
