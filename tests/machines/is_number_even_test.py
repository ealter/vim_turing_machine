import pytest

from vim_turing_machine.constants import BLANK_CHARACTER
from vim_turing_machine.constants import NO_FINAL_STATE
from vim_turing_machine.constants import YES_FINAL_STATE
from vim_turing_machine.machines.is_number_even import number_is_even_state_transitions
from vim_turing_machine.turing_machine import TuringMachine


def assert_tape(machine, expected_tape):
    # Ignore any blanks at the end
    assert expected_tape == ''.join(machine.tape).rstrip(BLANK_CHARACTER)


def run_machine(transitions, tape):
    machine = TuringMachine(list(transitions), quiet=True)
    machine.run(tape[:], max_steps=10000)

    assert_tape(machine, tape)

    return machine


@pytest.mark.parametrize('tape, is_even', [
    ('', False),
    ('1', False),
    ('0', True),
    ('1001', False),
    ('1010', True),
])
def test_is_number_even(tape, is_even):
    machine = run_machine(number_is_even_state_transitions, tape)
    if is_even:
        assert machine.current_state == YES_FINAL_STATE
    else:
        assert machine.current_state == NO_FINAL_STATE
