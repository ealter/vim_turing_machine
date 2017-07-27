from collections import namedtuple

from vim_turing_machine.constants import BACKWARDS
from vim_turing_machine.constants import FORWARDS
from vim_turing_machine.constants import INVALID_STATE_CHARACTERS
from vim_turing_machine.constants import VALID_CHARACTERS
from vim_turing_machine.constants import VIM_NEXT_STATE


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

    def to_vim(self):
        """Returns vim command mapping of this transition"""
        return (
            '_{}-{}:{}{}{}{}'
        ).format(
            self.previous_state,
            self.previous_character,
            self._change_state_to(),
            self._change_tape_to(),
            self._move_pointer(),
            VIM_NEXT_STATE,
        )

    def _change_state_to(self):
        """Returns the vim commands to change current state to next"""
        return '`k"_C{}'.format(self.next_state)

    def _change_tape_to(self):
        """Returns the vim commands to change current tape value to next"""
        return '`t"_cw{}'.format(self.next_character)

    def _move_pointer(self):
        """Returns the vim commands to move the tape after transition"""
        if self.tape_pointer_direction == FORWARDS:
            return '`twmt'
        else:
            return '`tbmt',
