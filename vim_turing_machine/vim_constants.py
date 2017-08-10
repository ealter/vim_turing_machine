VIM_MACHINE_FILENAME = 'machine.vim'

VIM_NEXT_STATE = '`ny$@"'

VIM_MOVE_TAPE_FORWARDS = '`tWmt'

VIM_MOVE_TAPE_BACKWARDS = '`tBmt'

VIM_RUN_REGISTER = '@"'

VIM_TAPE_WRAP_POSITION = 40

VIM_LOG_TAPE_AND_STATE = '`ly$@"'


def create_pointer(name, direction='j'):
    """Creates a mark to a particular place on the tape."""
    return '`h/_{name}:\rn{direction}m{name}'.format(name=name, direction=direction)


VIM_POINTERS = ''.join([
    create_pointer('t'),
    create_pointer('l'),
    create_pointer('k'),
    create_pointer('o'),
    create_pointer('p'),
    create_pointer('s', direction=''),
    create_pointer('n'),
    create_pointer('e', direction='k'),
])

VIM_TEMPLATE = """0/_v1\rnf-ly$@"

### launch with ggyy@" ###

# Init pointers
_v1-gg0mh{pointers}`ny$@"

_o:  # Output


_k:  # Current state
{initial_state}

_t:  # Current tape
{initial_tape}
notvalid\|--addlinetotape
_e:  # End of tape. Pointer is 1 line above this

_n:  # Next state transition. Usage: `ny$@"
{logging}`t"tyiW`ky$`s/_"-t\|---\rf:ly$@"

_p:  # Print state. Usage: `py$@"
`ky$`op

_l:  # Log the tape and state Usage: `ly$@"
`tyipGopdd`kyyGp

_s:  # State transitions
{state_transitions}
# End State transitions
# Add an extra line to the end of the tape
_--addlinetotape: `eO{characters_per_line}iX 0mt`ny$@"

# Print state when unknown transition
_---: `py$@"

# vim: set whichwrap+=b,s
"""
