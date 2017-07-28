import pytest

from vim_turing_machine.machines.merge_business_hours.decode_hours import decode_hours


def test_encode_hours():
    assert decode_hours('{}{}'.format('01010', '11111'), 5) == [[10, 31]]
