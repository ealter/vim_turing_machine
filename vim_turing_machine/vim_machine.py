from vim_turing_machine.constants import FORWARDS
from vim_turing_machine.constants import BACKWARDS
from vim_turing_machine.vim_constants import VIM_NEXT_STATE
from vim_turing_machine.vim_constants import VIM_TEMPLATE
from vim_turing_machine.vim_constants import VIM_MACHINE_FILENAME
from vim_turing_machine.turing_machine import TuringMachine


class VimStateTransitionAdapter(object):

    def __init__(self, state_transition):
        self.st = state_transition

    def to_vim(self):
        """Returns vim command mapping of this transition"""
        return (
            '_{}-{}:{}{}{}{}'
        ).format(
            self.st.previous_state,
            self.st.previous_character,
            self._change_state_to(),
            self._change_tape_to(),
            self._move_pointer(),
            VIM_NEXT_STATE,
        )

    def _change_state_to(self):
        """Returns the vim commands to change current state to next"""
        return '`k"_C{}'.format(self.st.next_state)

    def _change_tape_to(self):
        """Returns the vim commands to change current tape value to next"""
        return '`t"_cw{}'.format(self.st.next_character)

    def _move_pointer(self):
        """Returns the vim commands to move the tape after transition"""
        if self.st.tape_pointer_direction == FORWARDS:
            return '`tf lmt'
        elif self.st.tape_pointer_direction == BACKWARDS:
            return '`tF hmt'
        else:
            return ''


class VimTuringMachine(TuringMachine):

    def run(self, initial_tape):
        self.initialize_machine(initial_tape)

        with open(VIM_MACHINE_FILENAME, 'w') as machine:
            machine.write(VIM_TEMPLATE.format(
                initial_state=self._current_state,
                initial_tape=' '.join(self._tape+2*[' ']),
                state_transitions='\n'.join(
                    [
                        VimStateTransitionAdapter(state_transition).to_vim()
                        for state_transition in self._state_transitions
                    ]
                )
            ).replace('@"', '' if self._debug else '@"'))

        print('Machine written to {}'.format(VIM_MACHINE_FILENAME))
