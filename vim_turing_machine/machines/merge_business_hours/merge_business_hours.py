"""Our tape is defined in multiple segments, each separated by a blank character.

INPUT OUTPUT SCRATCH_SPACE

They are defined as follows:
    Input: The initial input to the program encoded in a series of 5-bit
        numbers. (start_1, end_1), (start_2, end_2) ...
"""
import itertools
import sys

from vim_turing_machine.constants import BLANK_CHARACTER
from vim_turing_machine.constants import INITIAL_STATE
from vim_turing_machine.constants import NO_FINAL_STATE
from vim_turing_machine.constants import VALID_CHARACTERS
from vim_turing_machine.constants import YES_FINAL_STATE
from vim_turing_machine.struct import BACKWARDS
from vim_turing_machine.struct import DO_NOT_MOVE
from vim_turing_machine.struct import FORWARDS
from vim_turing_machine.struct import StateTransition
from vim_turing_machine.turing_machine import TuringMachine


BITS_PER_NUMBER = 3  # TODO: change this to 5 bits


def merge_business_hours_transitions():
    # The first character should be an empty space. Let's move until we hit a non-empty space.
    transitions = [
        StateTransition(
            previous_state=INITIAL_STATE,
            previous_character=BLANK_CHARACTER,
            next_state=INITIAL_STATE,
            next_character=BLANK_CHARACTER,
            tape_pointer_direction=FORWARDS,
        )
    ]

    BEGIN_MOVE = 'BeginInitialMove'

    # We begin the program by copying the first hours pair into the output array
    transitions.extend(
        copy_bits_to_end_of_output(
            initial_state=INITIAL_STATE,
            num_bits=BITS_PER_NUMBER * 3,  # Copy (opening, closing, opening) to the output array
            final_state=BEGIN_MOVE,
        )
    )

    transitions.extend(
        compare_two_sequential_numbers(
            initial_state=BEGIN_MOVE,
            greater_than_or_equal_to_state=YES_FINAL_STATE,
            less_than_state=NO_FINAL_STATE,
        )
    )

    return transitions


def invert_bit(bit_value):
    if bit_value == '0':
        return '1'
    elif bit_value == '1':
        return '0'
    else:
        raise AssertionError('Invalid bit {}'.format(bit_value))


def invert_direction(direction):
    if direction == BACKWARDS:
        return FORWARDS
    elif direction == FORWARDS:
        return BACKWARDS
    else:
        raise AssertionError('Invalid direction {}'.format(direction))


def noop_when_non_blank(state, direction):
    return (
        StateTransition(
            previous_state=state,
            previous_character='0',
            next_state=state,
            next_character='0',
            tape_pointer_direction=direction,
        ),
        StateTransition(
            previous_state=state,
            previous_character='1',
            next_state=state,
            next_character='1',
            tape_pointer_direction=direction,
        ),
    )


def move_n_bits(initial_state, direction, final_state, num_bits):
    """Moves 'num_bits' in the specified direction. Errors if it encounters a
    blank space while doing so. Ends in the final_state."""
    def state_name(bit_index):
        if bit_index == 0:
            return initial_state
        elif bit_index == num_bits:
            return final_state
        else:
            return '{}MovingBit{}'.format(initial_state, bit_index)

    return itertools.chain.from_iterable([
        [
            StateTransition(
                previous_state=state_name(bit_index),
                previous_character=bit_value,
                next_state=state_name(bit_index + 1),
                next_character=bit_value,
                tape_pointer_direction=(
                    direction
                    if bit_index < num_bits - 1
                    else DO_NOT_MOVE
                ),
            )
            for bit_index in range(num_bits)
        ]
        for bit_value in ['0', '1']
    ])


def move_to_blank_spaces(initial_state, final_state, final_character, final_direction, direction, num_blanks):
    """Moves along the array until it hits a certain number of blank spaces.

    :param str initial_state: The state used to trigger this code
    :param str final_state: The state we should finish with
    :param str final_character: The character we should write on that state transition
    :param int final_direction: Which direction we should move at the end
    :param int direction: Which direction we should search in
    :param int num_blanks: How many blanks to search for
    """

    def state_name(blank_num):
        return '{}Searching{}'.format(initial_state, blank_num)

    transitions = [
        # Rename our current state
        StateTransition(
            previous_state=initial_state,
            previous_character=character,
            next_state=state_name(blank_num=0),
            next_character=character,
            tape_pointer_direction=DO_NOT_MOVE,
        )
        for character in VALID_CHARACTERS
    ]

    for blank_num in range(num_blanks):
        transitions.extend(
            # If we're looking for the first blank, then keep going until we hit it
            noop_when_non_blank(state_name(blank_num=blank_num), direction=direction)
        )

        if blank_num == num_blanks - 1:
            # This is the last blank
            transitions.append(
                StateTransition(
                    previous_state=state_name(blank_num),
                    previous_character=BLANK_CHARACTER,
                    next_state=final_state,
                    next_character=final_character,
                    tape_pointer_direction=final_direction,
                )
            )
        else:
            # This is not the last blank
            transitions.append(
                StateTransition(
                    previous_state=state_name(blank_num),
                    previous_character=BLANK_CHARACTER,
                    next_state=state_name(blank_num + 1),
                    next_character=BLANK_CHARACTER,
                    tape_pointer_direction=direction,
                )
            )

    return transitions


def copy_bits_to_end_of_output(initial_state, num_bits, final_state):
    """
    :param string initial_state: The state used before we start to move
    :param int num_bits: The number of bits to copy
    :param StateTransition final_state: The state to finish with when we are done copying

    Note: This overwrites the copied section with blanks.

    At the end of copying, we will end up at the end of the output section.

    :rtype: [StateTransition]
    """
    def state_name(bit_index):
        if bit_index == 0:
            return initial_state
        else:
            return '{}Copy{}'.format(initial_state, bit_index)

    def copy_bit(bit_index, bit_value):
        base_copying_state = '{}Bit{}'.format(state_name(bit_index + 1), bit_value)

        return [
            # Let's start copying the character. Note how we replace it with a blank.
            StateTransition(
                previous_state=state_name(bit_index),
                previous_character=bit_value,
                next_state='{}Forward'.format(base_copying_state),
                next_character=BLANK_CHARACTER,
                tape_pointer_direction=FORWARDS,
            ),

            *move_to_blank_spaces(
                initial_state='{}Forward'.format(base_copying_state),
                # If we're on the last character, don't go backwards
                final_state=(
                    '{}Backwards'.format(base_copying_state)
                    if bit_index < num_bits - 1
                    else final_state
                ),
                final_character=bit_value,
                final_direction=DO_NOT_MOVE,
                direction=FORWARDS,
                num_blanks=2,
            ),
            *move_to_blank_spaces(
                initial_state='{}Backwards'.format(base_copying_state),
                final_state=state_name(bit_index + 1),
                final_character=BLANK_CHARACTER,
                final_direction=FORWARDS,
                direction=BACKWARDS,
                num_blanks=2,
            ),
        ]

    return itertools.chain.from_iterable(
        (
            *copy_bit(bit_index, bit_value='0'),
            *copy_bit(bit_index, bit_value='1'),
        )
        for bit_index in range(num_bits)
    )


def compare_two_sequential_numbers(initial_state, greater_than_or_equal_to_state, less_than_state):
    """
    If the earlier number is greater than or equal to the later number, this
    will end in the greater_than_or_equal_to_state. If the earlier number is
    less than the later number, this will end in the less_than_state.

    Precondition: The cursor is at the end of the output array
    Postcondition: The cursor is at the end of the output array
    """

    def already_have_one_bit_state(bit_index, bit_value):
        """This means that we've read a 'bit_value' at 'bit_index'. We are
        currently searching for the equivalent bit in the other number."""
        return '{}BitIndex{}BitValue{}'.format(initial_state, bit_index, bit_value)

    def about_to_read_first_bit_state(bit_index):
        """This means that we're about to start reading/comparing the next bit
        index. We always immediately transition from this state to the
        'already_have_one_bit_state' after reading its value."""
        if bit_index == BITS_PER_NUMBER:
            # At this point, we know that the numbers are equal since we've compared every bit.
            return greater_than_or_equal_to_state
        else:
            return '{}BitIndex{}'.format(initial_state, bit_index)

    def about_to_compare_bits_state(bit_index, bit_value):
        """Our cursor is over the other bit we want to compare this one too."""
        return '{}BitIndex{}CompareWithBitValue{}'.format(initial_state, bit_index, bit_value)

    # Begin by moving to the beginning of the 2nd number.
    transitions = list(
        move_n_bits(
            initial_state=initial_state,
            direction=BACKWARDS,
            final_state=about_to_read_first_bit_state(bit_index=0),
            num_bits=BITS_PER_NUMBER,
        )
    )

    direction = BACKWARDS

    # Then begin comparing the digits one by one from largest to smallest
    for bit_index in range(BITS_PER_NUMBER):
        for bit_value in ['0', '1']:
            for transition in transitions:
                print(transition)

            transitions.append(
                # Read the current bit
                StateTransition(
                    previous_state=about_to_read_first_bit_state(bit_index),
                    previous_character=bit_value,
                    next_state=already_have_one_bit_state(bit_index, bit_value),
                    next_character=bit_value,
                    tape_pointer_direction=direction,
                )
            )

            # Then go to the equivalent bit in the other number. We already
            # moved 1 space in that direction.
            transitions.extend(
                move_n_bits(
                    initial_state=already_have_one_bit_state(bit_index, bit_value),
                    direction=direction,
                    final_state=about_to_compare_bits_state(bit_index, bit_value),
                    num_bits=BITS_PER_NUMBER - 1,
                )
            )

            # We've already read the 2nd number and now we're comparing it to
            # the first. Now finally do the comparison
            transitions.append(
                # If the numbers are equal
                StateTransition(
                    previous_state=about_to_compare_bits_state(bit_index, bit_value),
                    previous_character=bit_value,
                    next_state=about_to_read_first_bit_state(bit_index + 1),
                    next_character=bit_value,
                    tape_pointer_direction=invert_direction(direction),
                )
            )

            transitions.append(
                # If the numbers are not equal
                StateTransition(
                    previous_state=about_to_compare_bits_state(bit_index, bit_value),
                    previous_character=invert_bit(bit_value),
                    next_state=(
                        greater_than_or_equal_to_state
                        if (
                            (bit_value == '1' and direction == FORWARDS) or
                            (bit_value == '0' and direction == BACKWARDS)
                        )
                        else less_than_state
                    ),
                    next_character=invert_bit(bit_value),
                    tape_pointer_direction=invert_direction(direction),
                )
            )

    return transitions


if __name__ == '__main__':
    merge_business_hours = TuringMachine(merge_business_hours_transitions(), debug=True)
    merge_business_hours.run(initial_tape=sys.argv[1], max_steps=500)
