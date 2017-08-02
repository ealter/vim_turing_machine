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

    def __init__(self, state_transitions, debug=False, quiet=False):
        validate_state_transitions(state_transitions)

        self._state_transitions = state_transitions
        self._state_transition_mapping = {
            (state.previous_state, state.previous_character): state
            for state in state_transitions
        }
        self._debug = debug
        self._quiet = quiet
        self.initialize_machine(tape=[])

    def initialize_machine(self, tape, initial_cursor_position=0):
        self.tape = list(tape)[:]  # Copy the initial tape since we mutate it
        self.cursor_position = initial_cursor_position
        self.current_state = INITIAL_STATE
        self._num_steps = 0

    def get_state_transition(self):
        try:
            return self._state_transition_mapping[
                (self.current_state, self.tape[self.cursor_position])
            ]
        except KeyError:
            raise MissingStateTransition(
                (self.current_state, self.tape[self.cursor_position])
            )

    def step(self):
        """This implements an infinitely long tape in the right direction, but
        will error if you go beyond position 0"""
        transition = self.get_state_transition()

        self.tape[self.cursor_position] = transition.next_character

        self.cursor_position += transition.tape_pointer_direction

        if self.cursor_position < 0:
            raise NegativeTapePositionException

        # Make sure we haven't run more than 1 past the end of the tape. This
        # should never happen since we append to the tape over time.
        assert self.cursor_position <= len(self.tape)

        if self.cursor_position >= len(self.tape):
            # Fake the infinite tape by adding a blank character under the
            # cursor.
            self.tape.append(BLANK_CHARACTER)

        self.current_state = transition.next_state

        if self.current_state in FINAL_STATES:
            self.final_state()
        elif self._debug:
            self.print_tape()

    def final_state(self):
        if not self._quiet:
            print('Program complete. Final state: {}'.format(self.current_state))
            print(
                'The program completed in {} steps using a machine with {} transitions'.format(
                    self._num_steps,
                    len(self._state_transitions)
                )
            )
            self.print_tape()

        raise StopIteration

    def run(self, initial_tape, max_steps=None, initial_cursor_position=0):
        self.initialize_machine(initial_tape, initial_cursor_position=initial_cursor_position)

        if self._debug:
            self.print_tape()

        try:
            while(True):
                self.step()
                self._num_steps += 1

                if max_steps is not None and self._num_steps >= max_steps:
                    raise TooManyStepsException
        except StopIteration:
            pass

    def print_tape(self):
        tape = ''
        for i, character in enumerate(self.tape):
            if i == self.cursor_position:
                tape += '{}{}{}{}'.format(colored.bg('red'), colored.fg('white'), character, colored.attr('reset'))
            else:
                tape += character

            if i != len(self.tape) - 1:
                tape += ' | '

        print(tape)
        print('State: {}'.format(self.current_state))
        print()  # Add empty line


def validate_state_transitions(state_transitions):
    seen = defaultdict(list)

    for transition in state_transitions:
        transition.validate()

        key = (transition.previous_state, transition.previous_character)
        seen[key].append(transition)

    for transitions in seen.values():
        if len(transitions) > 1:
            raise DuplicateStateTransitionException(transitions)
