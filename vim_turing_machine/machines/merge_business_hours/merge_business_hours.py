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
from vim_turing_machine.constants import YES_FINAL_STATE
from vim_turing_machine.struct import BACKWARDS
from vim_turing_machine.struct import FORWARDS
from vim_turing_machine.struct import StateTransition
from vim_turing_machine.turing_machine import TuringMachine


ADVANCE_TO_END_OF_NUMBER = 'onward!'
FOUND_END_OF_NUMBER = 'eof'
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

    def backtracking_state(bit_index):
        if bit_index == num_bits - 1:
            return final_state
        else:
            return '{}Backtracking{}'.format(initial_state, bit_index)

    def copy_bit(bit_index, bit_value):
        base_copying_state = '{}Bit{}'.format(state_name(bit_index + 1), bit_value)

        return (
            # Let's start copying the character. Note how we replace it with a blank.
            StateTransition(
                previous_state=state_name(bit_index),
                previous_character=bit_value,
                next_state=base_copying_state,
                next_character=BLANK_CHARACTER,
                tape_pointer_direction=FORWARDS,
            ),

            # If we're looking for the first blank, then keep going until we hit it
            *noop_when_non_blank(base_copying_state, direction=FORWARDS),

            # With this first blank, we need to keep looking for the next one
            StateTransition(
                previous_state=base_copying_state,
                previous_character=BLANK_CHARACTER,
                next_state='{}Blank1'.format(base_copying_state),
                next_character=BLANK_CHARACTER,
                tape_pointer_direction=FORWARDS,
            ),

            # After the first blank, we've hit the end of the input array. Now
            # we're looking for the second which will denote the end of the
            # output array
            *noop_when_non_blank(
                '{}Blank1'.format(base_copying_state),
                direction=FORWARDS,
            ),

            # Now things get fun. We've finally hit the end of the output
            # array! We can now write the character we were carrying.
            StateTransition(
                previous_state='{}Blank1'.format(base_copying_state),
                previous_character=BLANK_CHARACTER,
                next_state=backtracking_state(bit_index),
                next_character=bit_value,
                tape_pointer_direction=BACKWARDS,
            ),

            # Now search for the end of the output array (i.e. after we hit 2 blanks)

            # If we're looking for the first blank, then keep going until we hit it
            *noop_when_non_blank(base_copying_state, direction=FORWARDS),

            # With this first blank, we need to keep looking for the next one
            StateTransition(
                previous_state=base_copying_state,
                previous_character=BLANK_CHARACTER,
                next_state='{}Blank1'.format(base_copying_state),
                next_character=BLANK_CHARACTER,
                tape_pointer_direction=FORWARDS,
            ),

            # After the first blank, we've hit the end of the input array. Now
            # we're looking for the second which will denote the end of the
            # output array
            *noop_when_non_blank(
                '{}Blank1'.format(base_copying_state),
                direction=FORWARDS,
            ),

            # Now things get fun. We've finally hit the end of the output
            # array! We can now write the character we were carrying.
            StateTransition(
                previous_state='{}Blank1'.format(base_copying_state),
                previous_character=BLANK_CHARACTER,
                next_state=backtracking_state(bit_index),
                next_character=bit_value,
                tape_pointer_direction=BACKWARDS,
            ),

            # Then we backtrack back to the beginning of the input again (i.e. until we hit 2 blank spaces)

            # Start looking for the first space
            *noop_when_non_blank(
                backtracking_state(bit_index),
                direction=BACKWARDS,
            ),

            # When we hit the first space, start looking for the next one
            StateTransition(
                previous_state=backtracking_state(bit_index),
                previous_character=BLANK_CHARACTER,
                next_state='{}Blank1'.format(backtracking_state(bit_index)),
                next_character=BLANK_CHARACTER,
                tape_pointer_direction=BACKWARDS,
            ),

            # Now keep looking for the next blank
            *noop_when_non_blank(
                '{}Blank1'.format(backtracking_state(bit_index)),
                direction=BACKWARDS,
            ),

            # When we hit the 2nd blank, we're ready to transition back to copying the next character
            StateTransition(
                previous_state='{}Blank1'.format(backtracking_state(bit_index)),
                previous_character=BLANK_CHARACTER,
                next_state=state_name(bit_index),
                next_character=BLANK_CHARACTER,
                tape_pointer_direction=FORWARDS,
            ),
        )

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
