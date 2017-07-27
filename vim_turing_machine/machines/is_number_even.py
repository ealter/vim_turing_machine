import sys

from vim_turing_machine.constants import BLANK_CHARACTER
from vim_turing_machine.constants import INITIAL_STATE
from vim_turing_machine.constants import NO_FINAL_STATE
from vim_turing_machine.constants import WILDCARD_CHARACTER
from vim_turing_machine.constants import YES_FINAL_STATE
from vim_turing_machine.struct import BACKWARDS
from vim_turing_machine.struct import FORWARDS
from vim_turing_machine.struct import StateTransition
from vim_turing_machine.turing_machine import TuringMachine


ADVANCE_TO_END_OF_NUMBER = 'onward!'
FOUND_END_OF_NUMBER = 'eof'


number_is_even_state_transitions = (
    # A number is not even if the initial tape is blank.
    StateTransition(
        previous_state=INITIAL_STATE,
        previous_character=BLANK_CHARACTER,
        next_state=NO_FINAL_STATE,
        next_character=BLANK_CHARACTER,
        tape_pointer_direction=FORWARDS,
    ),

    # But any other number initially means that we should go find the end of the array
    StateTransition(
        previous_state=INITIAL_STATE,
        previous_character=WILDCARD_CHARACTER,
        next_character=WILDCARD_CHARACTER,
        next_state=ADVANCE_TO_END_OF_NUMBER,
        tape_pointer_direction=FORWARDS,
    ),

    # Once we're looking for the end of the number, go until we hit a blank
    StateTransition(
        previous_state=ADVANCE_TO_END_OF_NUMBER,
        previous_character=WILDCARD_CHARACTER,
        next_character=WILDCARD_CHARACTER,
        next_state=ADVANCE_TO_END_OF_NUMBER,
        tape_pointer_direction=FORWARDS,
    ),

    # Once we're looking for the end of the number, go until we hit a blank.
    # Then backtrack 1 space.
    StateTransition(
        previous_state=ADVANCE_TO_END_OF_NUMBER,
        previous_character=BLANK_CHARACTER,
        next_character=BLANK_CHARACTER,
        next_state=FOUND_END_OF_NUMBER,
        tape_pointer_direction=BACKWARDS,
    ),

    # Now that we're on the last character, check if it is even or odd
    StateTransition(
        previous_state=FOUND_END_OF_NUMBER,
        previous_character='0',
        next_character='0',
        next_state=YES_FINAL_STATE,
        tape_pointer_direction=FORWARDS,
    ),
    StateTransition(
        previous_state=FOUND_END_OF_NUMBER,
        previous_character='1',
        next_character='1',
        next_state=NO_FINAL_STATE,
        tape_pointer_direction=FORWARDS,
    ),
)


if __name__ == '__main__':
    even_odd_turing_machine = TuringMachine(number_is_even_state_transitions, debug=True)
    even_odd_turing_machine.run(initial_tape=sys.argv[1])
