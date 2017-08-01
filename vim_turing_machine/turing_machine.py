from collections import defaultdict

import colored

from vim_turing_machine.constants import BLANK_CHARACTER
from vim_turing_machine.constants import FINAL_STATES
from vim_turing_machine.constants import INITIAL_STATE


class NegativeTapePositionException(Exception):
    pass


class MissingStateTransition(Exception):
    pass


class DuplicateStateTransitionException(Exception):
    pass


class TooManyStepsException(Exception):
    pass


class TuringMachine(object):

    def __init__(self, state_transitions, debug=False):
        validate_state_transitions(state_transitions)

        self._state_transitions = state_transitions
        self._state_transition_mapping = {
            (state.previous_state, state.previous_character): state
            for state in state_transitions
        }
        self._debug = debug
        self.initialize_machine(tape=[])

    def initialize_machine(self, tape):
        self._tape = list(tape)[:]  # Copy the initial tape since we mutate it
        self._cursor_position = 0
        self._current_state = INITIAL_STATE

    def get_state_transition(self):
        try:
            return self._state_transition_mapping[
                (self._current_state, self._tape[self._cursor_position])
            ]
        except KeyError:
            raise MissingStateTransition(
                (self._current_state, self._tape[self._cursor_position])
            )

    def step(self):
        """This implements an infinitely long tape in the right direction, but
        will error if you go beyond position 0"""
        transition = self.get_state_transition()

        self._tape[self._cursor_position] = transition.next_character

        self._cursor_position += transition.tape_pointer_direction

        if self._cursor_position < 0:
            raise NegativeTapePositionException

        # Make sure we haven't run more than 1 past the end of the tape. This
        # should never happen since we append to the tape over time.
        assert self._cursor_position <= len(self._tape)

        if self._cursor_position >= len(self._tape):
            # Fake the infinite tape by adding a blank character under the
            # cursor.
            self._tape.append(BLANK_CHARACTER)

        self._current_state = transition.next_state

        if self._current_state in FINAL_STATES:
            self.final_state()
        elif self._debug:
            self.print_tape()

    def final_state(self):
        print('Program complete. Final state: {}'.format(self._current_state))
        self.print_tape()
        raise StopIteration

    def run(self, initial_tape, max_steps=None):
        self.initialize_machine(initial_tape)

        if self._debug:
            self.print_tape()

        num_steps = 0

        try:
            while(True):
                self.step()
                num_steps += 1

                if max_steps is not None and num_steps >= max_steps:
                    raise TooManyStepsException
        except StopIteration:
            pass

    def print_tape(self):
        tape = ''
        for i, character in enumerate(self._tape):
            if i == self._cursor_position:
                tape += '{}{}{}{}'.format(colored.bg('red'), colored.fg('white'), character, colored.attr('reset'))
            else:
                tape += character

            if i != len(self._tape) - 1:
                tape += ' | '

        print(tape)
        print('State: {}'.format(self._current_state))
        print()  # Add empty line

    def get_tape(self):
        return self._tape


def validate_state_transitions(state_transitions):
    seen = defaultdict(list)

    for transition in state_transitions:
        transition.validate()

        key = (transition.previous_state, transition.previous_character)
        seen[key].append(transition)

    for transitions in seen.values():
        if len(transitions) > 1:
            raise DuplicateStateTransitionException(transitions)
