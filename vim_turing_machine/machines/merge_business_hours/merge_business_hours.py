"""Our tape is defined in multiple segments, each separated by a blank character.

INPUT OUTPUT SCRATCH_SPACE

They are defined as follows:
    Input: The initial input to the program encoded in a series of 5-bit
        numbers. (start_1, end_1), (start_2, end_2) ...
"""
import itertools
import re
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
            num_bits=3,
            next_state=YES_FINAL_STATE,
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


def copy_bits_to_end_of_output(initial_state, num_bits, next_state):
    """
    :param string initial_state: The state used before we start to move
    :param int num_bits: The number of bits to copy
    :param StateTransition next_state: The state to finish with when we are done copying

    Note: This overwrites the copied section with blanks

    :rtype: [StateTransition]
    """
    def state_name(i):
        if i == 0:
            return initial_state
        elif i == num_bits - 1:
            return next_state
        else:
            return '{}Copy{}'.format(initial_state, i)

    def state_to_encoded_bit(state):
        """A state name might be FooCopy5Bit0Bar in which case we want to return '0'"""
        assert 'Bit' not in initial_state  # Messes up the regex
        return re.search(r'Bit(\d+)', state).group(1)

    def state_to_bit_index(state):
        """Figures out which bit we are copying again given the state name.
        FooCopy5Bit0Bar would return '5'"""
        assert 'Copy' not in initial_state  # Messes up the regex
        return re.search(r'Copy(\d+)', state).group(1)

    def backtracking_state(bit_index_to_copy_next):
        return '{}Backtracking{}'.format(initial_state, bit_index_to_copy_next)

    # Create the transitions to say "Let's start copying this next character".
    start_copying_transitions = itertools.chain.from_iterable([
        (
            StateTransition(
                previous_state=state_name(i),
                previous_character='0',
                next_state='{}Bit0'.format(state_name(i + 1)),
                next_character=BLANK_CHARACTER,
                tape_pointer_direction=FORWARDS,
            ),
            StateTransition(
                previous_state=state_name(i),
                previous_character='1',
                next_state='{}Bit1'.format(state_name(i + 1)),
                next_character=BLANK_CHARACTER,
                tape_pointer_direction=FORWARDS,
            ),
        )
        for i in range(num_bits)
    ])

    # Now search for the end of the output array (i.e. after we hit 2 blanks)
    search_for_output_array_transitions = itertools.chain.from_iterable([
        (
            # If we're looking for the first blank, then keep going until we hit it
            *noop_when_non_blank(transition.next_state, direction=FORWARDS),

            # With this first blank, we need to keep looking for the next one
            StateTransition(
                previous_state=transition.next_state,
                previous_character=BLANK_CHARACTER,
                next_state='{}Blank1'.format(transition.next_state),
                next_character=BLANK_CHARACTER,
                tape_pointer_direction=FORWARDS,
            ),

            # After the first blank, we've hit the end of the input array. Now
            # we're looking for the second which will denote the end of the
            # output array
            *noop_when_non_blank(
                '{}Blank1'.format(transition.next_state),
                direction=FORWARDS,
            ),

            # Now things get fun. We've finally hit the end of the output
            # array! We can now write the character we were carrying.
            StateTransition(
                previous_state='{}Blank1'.format(transition.next_state),
                previous_character=BLANK_CHARACTER,
                next_state=backtracking_state(state_to_bit_index(transition.next_state)),
                next_character=state_to_encoded_bit(transition.next_state),
                tape_pointer_direction=BACKWARDS,
            ),
        )
        for transition in start_copying_transitions
    ])

    # Then we backtrack back to the beginning of the input again (i.e. until we hit 2 blank spaces)
    backtracking_transitions = itertools.chain.from_iterable([
        (
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
        for bit_index in range(num_bits)
    ])

    return itertools.chain(
        start_copying_transitions,
        search_for_output_array_transitions,
        backtracking_transitions,
    )


if __name__ == '__main__':
    merge_business_hours = TuringMachine(merge_business_hours_transitions(), debug=True)
    merge_business_hours.run(initial_tape=sys.argv[1])
