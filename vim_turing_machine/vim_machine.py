from vim_turing_machine.constants import BACKWARDS
from vim_turing_machine.constants import BLANK_CHARACTER
from vim_turing_machine.constants import FORWARDS
from vim_turing_machine.turing_machine import TuringMachine
from vim_turing_machine.vim_constants import VIM_LOG_TAPE_AND_STATE
from vim_turing_machine.vim_constants import VIM_MACHINE_FILENAME
from vim_turing_machine.vim_constants import VIM_MOVE_TAPE_BACKWARDS
from vim_turing_machine.vim_constants import VIM_MOVE_TAPE_FORWARDS
from vim_turing_machine.vim_constants import VIM_NEXT_STATE
from vim_turing_machine.vim_constants import VIM_POINTERS
from vim_turing_machine.vim_constants import VIM_RUN_REGISTER
from vim_turing_machine.vim_constants import VIM_TAPE_WRAP_POSITION
from vim_turing_machine.vim_constants import VIM_TEMPLATE


def create_initial_tape(input_tape):
    """Generates the initial tape by padding the input and wrapping"""
    padding_length = VIM_TAPE_WRAP_POSITION - len(input_tape) % VIM_TAPE_WRAP_POSITION
    input_tape += padding_length * [BLANK_CHARACTER]

    initial_tape = []
    for index, value in enumerate(input_tape):
        if index % VIM_TAPE_WRAP_POSITION == 0:
            initial_tape.append([])
        initial_tape[index // VIM_TAPE_WRAP_POSITION].append(value)

    return '\n'.join(' '.join(row) for row in initial_tape)


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
            return VIM_MOVE_TAPE_FORWARDS
        elif self.st.tape_pointer_direction == BACKWARDS:
            return VIM_MOVE_TAPE_BACKWARDS
        else:
            return ''


class VimTuringMachine(TuringMachine):

    def run(self, initial_tape, auto_step=True):
        """Generates vim machine in an output file"""
        self.initialize_machine(initial_tape)

        with open(VIM_MACHINE_FILENAME, 'w') as machine:
            machine.write(VIM_TEMPLATE.format(
                initial_state=self.current_state,
                initial_tape=create_initial_tape(self.tape),
                characters_per_line=VIM_TAPE_WRAP_POSITION,
                pointers=VIM_POINTERS,
                blank_character=BLANK_CHARACTER,
                logging=(
                    VIM_LOG_TAPE_AND_STATE if auto_step and self._debug else ''
                ),
                state_transitions='\n'.join(
                    VimStateTransitionAdapter(state_transition).to_vim()
                    for state_transition in self._state_transitions
                ),
            ).replace(VIM_RUN_REGISTER, VIM_RUN_REGISTER if auto_step else ''))

        print('Machine written to {}'.format(VIM_MACHINE_FILENAME))
