import pytest

from vim_turing_machine.constants import FORWARDS
from vim_turing_machine.struct import StateTransition
from vim_turing_machine.turing_machine import DuplicateStateTransitionException
from vim_turing_machine.turing_machine import validate_state_transitions


def test_invalid_state_transition():
    with pytest.raises(AssertionError):
        validate_state_transitions([
            StateTransition(
                previous_state='foo',
                previous_character='Not a valid character',
                next_state='bar',
                next_character='0',
                tape_pointer_direction=FORWARDS,
            )
        ])


def test_valid_states():
    validate_state_transitions(
        [
            StateTransition(
                previous_state='foo',
                previous_character='0',
                next_state='bar',
                next_character='0',
                tape_pointer_direction=FORWARDS,
            ),
            StateTransition(
                previous_state='foo',
                previous_character='1',
                next_state='bar',
                next_character='1',
                tape_pointer_direction=FORWARDS,
            ),
        ]
    )


def test_duplicate_states():
    state = StateTransition(
        previous_state='foo',
        previous_character='0',
        next_state='bar',
        next_character='0',
        tape_pointer_direction=FORWARDS,
    )
    with pytest.raises(DuplicateStateTransitionException):
        validate_state_transitions([state, state])
