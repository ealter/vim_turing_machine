# -*- coding: utf-8 -*-
from collections import namedtuple

# Tape pointer direction
FORWARDS = 1
BACKWARDS = -1


class StateTransition(namedtuple('StateTransition', [
    'previous_state',
    'previous_character',
    'next_state',
    'next_character',
    'tape_pointer_direction',
])):
    pass
