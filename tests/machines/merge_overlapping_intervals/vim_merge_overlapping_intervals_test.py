import subprocess

from vim_turing_machine.machines.merge_overlapping_intervals.decode_intervals import decode_intervals
from vim_turing_machine.machines.merge_overlapping_intervals.encode_intervals import encode_intervals
from vim_turing_machine.machines.merge_overlapping_intervals.merge_overlapping_intervals import MergeOverlappingIntervalsGenerator
from vim_turing_machine.vim_constants import VIM_MACHINE_FILENAME
from vim_turing_machine.vim_machine import VimTuringMachine


NUM_BITS = 3


def run_vim_machine(intervals):
    initial_tape = encode_intervals(intervals, NUM_BITS)

    gen = MergeOverlappingIntervalsGenerator(NUM_BITS)
    merge_overlapping_intervals = VimTuringMachine(gen.merge_overlapping_intervals_transitions(), debug=False)

    # Write to the vim machine file
    merge_overlapping_intervals.run(initial_tape=initial_tape)

    subprocess.run(
        [
            'vim',
            '-u',
            'vimrc',
            VIM_MACHINE_FILENAME,
            '-c',
            # Execute the vim machine and then save the resulting file
            ":execute 'normal gg0yy@\"' | :x",
        ],
        timeout=10,
        check=True,
    )


def read_contents_of_tape():
    with open(VIM_MACHINE_FILENAME, 'r') as f:
        tape_lines = []
        found_beginning_of_tape = False

        for line in f:
            # Look for the lines between '_t:' and 'notvalid'
            if line.startswith('_t:'):
                found_beginning_of_tape = True
            elif line.startswith('notvalid'):
                return convert_tape_to_string(tape_lines)
            elif found_beginning_of_tape:
                tape_lines.append(line)

    raise AssertionError('Could not find the tape')


def convert_tape_to_string(tape_lines):
    return ''.join(tape_lines).replace(' ', '').replace('\n', '')


def test_merge_intervals_in_vim():
    run_vim_machine([[1, 2], [2, 3], [5, 7]])
    tape = read_contents_of_tape()

    intervals = decode_intervals(tape, num_bits=NUM_BITS)
    assert intervals == [[1, 3], [5, 7]]
