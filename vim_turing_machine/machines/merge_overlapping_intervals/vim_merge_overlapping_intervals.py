import json
import sys

from vim_turing_machine.machines.merge_overlapping_intervals.encode_intervals import encode_intervals
from vim_turing_machine.machines.merge_overlapping_intervals.merge_overlapping_intervals import MergeOverlappingIntervalsGenerator
from vim_turing_machine.vim_machine import VimTuringMachine


if __name__ == '__main__':
    input_string = json.loads(sys.argv[1])
    num_bits = int(sys.argv[2])

    initial_tape = encode_intervals(input_string, num_bits)

    gen = MergeOverlappingIntervalsGenerator(num_bits)
    merge_overlapping_intervals = VimTuringMachine(gen.merge_overlapping_intervals_transitions(), debug=False)
    merge_overlapping_intervals.run(initial_tape=initial_tape)
