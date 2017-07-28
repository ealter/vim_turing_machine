VIM_MACHINE_FILENAME = 'machine.vim'

VIM_NEXT_STATE = '`ny$@"'

VIM_MOVE_TAPE_FORWARDS = '`twmt'

VIM_MOVE_TAPE_BACKWARDS = '`tbmt'

VIM_RUN_REGISTER = '@"'

VIM_TAPE_WRAP_POSITION = 40

VIM_TAPE_NUM_ROWS = 4

VIM_TAPE_MAX_LENGTH = VIM_TAPE_WRAP_POSITION * VIM_TAPE_NUM_ROWS

VIM_TEMPLATE = """0/_v1\rnf-ly$@"

### launch with ggyy@" ###

# Init pointers
_v1-gg0mh`h/_t\rnjmt`h/_k\rnjmk`h/_o\rnjmo`h/_p\rnjmp`h/_s\rnms`h/_n:\rnjmn`ny$@"

_o:  # Output


_k:  # Current state
{initial_state}

_t:  # Current tape
{initial_tape}

_n:  # Next state transition. Usage: `ny$@"
`t"tyiw`ky$`s/_\V\("-t\|---\)\rf:ly$@"

_p:  # Print state. Usage: `py$@"
`ky$`op

_s:  # State transitions
{state_transitions}
# End State transitions
# Print state when unknown transition
_---: `py$@"

# vim: set whichwrap+=b,s
"""