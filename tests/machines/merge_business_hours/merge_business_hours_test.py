from unittest import mock

import pytest

import vim_turing_machine.machines.merge_business_hours.merge_business_hours
import vim_turing_machine.struct
import vim_turing_machine.turing_machine
from vim_turing_machine.constants import INITIAL_STATE
from vim_turing_machine.constants import NO_FINAL_STATE
from vim_turing_machine.constants import YES_FINAL_STATE
from vim_turing_machine.machines.merge_business_hours.decode_hours import decode_hours
from vim_turing_machine.machines.merge_business_hours.encode_hours import encode_hours
from vim_turing_machine.machines.merge_business_hours.merge_business_hours import invert_bit
from vim_turing_machine.machines.merge_business_hours.merge_business_hours import invert_direction
from vim_turing_machine.machines.merge_business_hours.merge_business_hours import MergeBusinessHoursGenerator
from vim_turing_machine.struct import BACKWARDS
from vim_turing_machine.struct import FORWARDS
from vim_turing_machine.turing_machine import TuringMachine


@pytest.yield_fixture(autouse=True)
def mock_blank_character():
    """Change the blank character to be a space so that it's easier to write test cases."""
    with mock.patch.object(
        vim_turing_machine.turing_machine,
        'BLANK_CHARACTER',
        ' ',
    ):
        with mock.patch.object(
            vim_turing_machine.struct,
            'VALID_CHARACTERS',
            ('0', '1', ' '),
        ):
            with mock.patch.object(
                vim_turing_machine.machines.merge_business_hours.merge_business_hours,
                'BLANK_CHARACTER',
                ' ',
            ):
                with mock.patch.object(
                    vim_turing_machine.machines.merge_business_hours.merge_business_hours,
                    'VALID_CHARACTERS',
                    ('0', '1', ' '),
                ):
                    yield


@pytest.fixture
def merger():
    return MergeBusinessHoursGenerator(num_bits=3)


def run_machine(transitions, tape, initial_position=0, assert_tape_not_changed=False):
    machine = TuringMachine(list(transitions), quiet=True)
    machine.run(tape[:], max_steps=10000, initial_cursor_position=initial_position)

    if assert_tape_not_changed:
        assert_tape(machine, tape)

    return machine


def assert_cursor_at_end_of_output(machine):
    end = len(machine.tape) - 1
    while end > 0 and machine.tape[end] == ' ':
        end -= 1

    assert machine.cursor_position == end


def assert_cursor_is_at_beginning_of_input(machine):
    i = 0
    while i < len(machine.tape) and machine.tape[i] == ' ':
        i += 1

    assert machine.cursor_position == i


def assert_tape(machine, expected_tape):
    # Ignore any blanks at the end
    assert expected_tape == ''.join(machine.tape).rstrip()


def test_invert_bit():
    assert invert_bit('0') == '1'
    assert invert_bit('1') == '0'
    with pytest.raises(AssertionError):
        invert_bit('not_valid')


def test_invert_direction():
    assert invert_direction(FORWARDS) == BACKWARDS
    assert invert_direction(BACKWARDS) == FORWARDS
    with pytest.raises(AssertionError):
        invert_direction('not_valid')


def test_move_n_bits(merger):
    machine = run_machine(
        merger.move_n_bits(
            initial_state=INITIAL_STATE,
            direction=FORWARDS,
            final_state=YES_FINAL_STATE,
            num_bits=4,
        ),
        tape='01010111',
        assert_tape_not_changed=True,
    )

    assert machine.cursor_position == 4


def test_move_to_blank_spaces(merger):
    machine = run_machine(
        merger.move_to_blank_spaces(
            initial_state=INITIAL_STATE,
            direction=FORWARDS,
            final_state=YES_FINAL_STATE,
            final_character=' ',
            final_direction=BACKWARDS,
            num_blanks=2,
        ),
        tape='01 1111 10',
        assert_tape_not_changed=True,
    )

    assert machine.cursor_position == 6  # End of the 1111


def test_copy_bits_to_end_of_output(merger):
    machine = run_machine(
        merger.copy_bits_to_end_of_output(
            initial_state=INITIAL_STATE,
            num_bits=3,
            final_state=YES_FINAL_STATE,
        ),
        tape='10111 01',
    )

    assert_tape(machine, '   11 01101')
    assert_cursor_at_end_of_output(machine)


@pytest.mark.parametrize('tape, final_state', [
    ('101 100110', NO_FINAL_STATE),
    ('101 100100', YES_FINAL_STATE),
    ('101 111100', YES_FINAL_STATE),
])
def test_compare_two_sequential_numbers(merger, tape, final_state):
    machine = run_machine(
        merger.compare_two_sequential_numbers(
            initial_state=INITIAL_STATE,
            greater_than_or_equal_to_state=YES_FINAL_STATE,
            less_than_state=NO_FINAL_STATE,
        ),
        tape=tape,
        initial_position=len(tape) - 1,
        assert_tape_not_changed=True,
    )

    assert_cursor_at_end_of_output(machine)
    assert machine.current_state == final_state


def test_erase_number(merger):
    machine = run_machine(
        merger.erase_number(
            initial_state=INITIAL_STATE,
            final_state=YES_FINAL_STATE,
        ),
        tape='100101110',
        initial_position=5,  # end of 101
    )

    assert machine.cursor_position == 2
    assert_tape(machine, '100   110')


def test_replace_number(merger):
    tape = '100101110'

    machine = run_machine(
        merger.replace_number(
            initial_state=INITIAL_STATE,
            final_state=YES_FINAL_STATE,
        ),
        tape=tape,
        initial_position=len(tape) - 1,
    )

    assert_tape(machine, '100110')
    assert_cursor_at_end_of_output(machine)


@pytest.mark.parametrize('tape, final_state', [
    (' 100 101101', NO_FINAL_STATE),
    ('  100101101', YES_FINAL_STATE),
])
def test_check_if_there_is_any_input_left(merger, tape, final_state):
    machine = run_machine(
        merger.check_if_there_is_any_input_left(
            initial_state=INITIAL_STATE,
            final_state=NO_FINAL_STATE,  # The machine exits with Yes if there is no input left.
        ),
        tape=tape,
        initial_position=len(tape) - 1,
        assert_tape_not_changed=True,
    )

    assert_cursor_is_at_beginning_of_input(machine)
    assert machine.current_state == final_state


@pytest.mark.parametrize('initial_tape, final_tape', [
    (' 100 001010001', '     001100'),  # 2nd pair's closing hour is larger
    (' 010 001110001', '     001110'),  # 2nd pair's closing hour is smaller
    (' 110 001110001', '     001110'),  # 2nd pair's closing hour is equal
])
def test_copy_closing_hour_and_merge(merger, initial_tape, final_tape):
    machine = run_machine(
        merger.copy_closing_hour_and_merge(
            initial_state=INITIAL_STATE,
            final_state=YES_FINAL_STATE,
        ),
        tape=initial_tape,
        initial_position=len(initial_tape) - 1,
    )

    assert_cursor_at_end_of_output(machine)
    assert_tape(machine, final_tape)


def test_copy_closing_hour_without_merging(merger):
    tape = ' 111 000010110'
    machine = run_machine(
        merger.copy_closing_hour_without_merging(
            initial_state=INITIAL_STATE,
            final_state=YES_FINAL_STATE,
        ),
        tape=tape,
        initial_position=len(tape) - 1,
    )

    assert_cursor_at_end_of_output(machine)
    assert_tape(machine, '     000010110111')


@pytest.mark.parametrize('initial_hours, final_hours',
                         [
                             (
                                 [[0, 1]],
                                 [[0, 1]],
                             ),
                             (
                                 [[0, 1], [5, 6]],
                                 [[0, 1], [5, 6]],
                             ),
                             (
                                 [[0, 5], [2, 3]],
                                 [[0, 5]],
                             ),
                             (
                                 [[1, 3], [3, 4], [4, 5], [6, 7]],
                                 [[1, 5], [6, 7]],
                             )
                         ]
                         )
def test_merge_business_hours(merger, initial_hours, final_hours):
    """The true integration test!"""
    tape = encode_hours(initial_hours, num_bits=3)
    machine = run_machine(
        merger.merge_business_hours_transitions(),
        tape=tape,
    )

    assert final_hours == decode_hours(''.join(machine.tape), num_bits=3)
