# -*- coding: utf-8 -*-
BLANK_CHARACTER = ' '
INITIAL_STATE = 'initial_state'
# If we do not define a state for the character in question, we can use the
# wildcard state. This allows us to DRY our state machine and group common
# states together.
WILDCARD_CHARACTER = '*'

YES_FINAL_STATE = 'YES'
NO_FINAL_STATE = 'NO'

FINAL_STATES = [YES_FINAL_STATE, NO_FINAL_STATE]
