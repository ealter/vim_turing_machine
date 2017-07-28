import sys

from vim_turing_machine.machines.is_number_even import number_is_even_state_transitions
from vim_turing_machine.vim_machine import VimTuringMachine

if __name__ == '__main__':
    even_odd_turing_machine = VimTuringMachine(number_is_even_state_transitions, debug=False)
    even_odd_turing_machine.run(initial_tape=sys.argv[1])
