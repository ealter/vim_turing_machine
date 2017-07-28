import sys

from vim_turing_machine.machines.merge_business_hours.merge_business_hours import merge_business_hours_transitions
from vim_turing_machine.vim_machine import VimTuringMachine


if __name__ == '__main__':
    merge_business_hours = VimTuringMachine(merge_business_hours_transitions(), debug=False)
    merge_business_hours.run(initial_tape=sys.argv[1])
