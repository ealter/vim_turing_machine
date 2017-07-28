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
from vim_turing_machine.constants import VALID_CHARACTERS
from vim_turing_machine.constants import YES_FINAL_STATE
from vim_turing_machine.struct import BACKWARDS
from vim_turing_machine.struct import DO_NOT_MOVE
from vim_turing_machine.struct import FORWARDS
from vim_turing_machine.struct import StateTransition
from vim_turing_machine.turing_machine import TuringMachine


BITS_PER_NUMBER = 5


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

    # We begin the program by copying the first hours pair into the output array
    transitions.extend(
        copy_bits_to_end_of_output(
            initial_state=INITIAL_STATE,
            num_bits=2,
            final_state=YES_FINAL_STATE,
        )
    )

    return transitions


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

    Note: This overwrites the copied section with blanks

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


if __name__ == '__main__':
    merge_business_hours = TuringMachine(merge_business_hours_transitions(), debug=True)
    merge_business_hours.run(initial_tape=sys.argv[1], max_steps=50)
