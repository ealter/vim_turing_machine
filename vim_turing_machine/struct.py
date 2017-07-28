from collections import namedtuple

from vim_turing_machine.constants import BACKWARDS
from vim_turing_machine.constants import FORWARDS
from vim_turing_machine.constants import INVALID_STATE_CHARACTERS
from vim_turing_machine.constants import VALID_CHARACTERS


class StateTransition(namedtuple('StateTransition', [
    'previous_state',
    'previous_character',
    'next_state',
    'next_character',
    'tape_pointer_direction',
])):
    def validate(self):
        assert self.tape_pointer_direction in (FORWARDS, BACKWARDS)
        assert self.previous_character in VALID_CHARACTERS
        assert self.next_character in VALID_CHARACTERS
        for invalid_char in INVALID_STATE_CHARACTERS:
            assert invalid_char not in self.previous_state
            assert invalid_char not in self.next_state
