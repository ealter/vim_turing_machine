import json
import sys

from vim_turing_machine.machines.merge_business_hours.encode_hours import encode_hours
from vim_turing_machine.machines.merge_business_hours.merge_business_hours import merge_business_hours_transitions
from vim_turing_machine.vim_machine import VimTuringMachine


if __name__ == '__main__':
    input_string = json.loads(sys.argv[1])
    num_bits = int(sys.argv[2])

    initial_tape = encode_hours(input_string, num_bits)

    merge_business_hours = VimTuringMachine(merge_business_hours_transitions(), debug=True)
    merge_business_hours.run(initial_tape=initial_tape)
