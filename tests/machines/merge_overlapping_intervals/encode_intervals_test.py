import pytest

from vim_turing_machine.machines.merge_overlapping_intervals.encode_intervals import encode_in_x_bits
from vim_turing_machine.machines.merge_overlapping_intervals.encode_intervals import encode_intervals


@pytest.mark.parametrize('number, encoded', [
    (0, '00000'),
    (10, '01010'),
    (31, '11111'),
])
def test_encode_in_x_bits(number, encoded):
    assert encode_in_x_bits(number, num_bits=5) == encoded


def test_encode_intervals():
    assert encode_intervals([(10, 31)], num_bits=5) == '{}{}'.format('01010', '11111')
