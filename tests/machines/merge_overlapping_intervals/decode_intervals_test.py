from vim_turing_machine.machines.merge_overlapping_intervals.decode_intervals import decode_intervals


def test_encode_intervals():
    assert decode_intervals('{}{}'.format('01010', '11111'), 5) == [[10, 31]]
