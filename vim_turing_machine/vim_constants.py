VIM_MACHINE_FILENAME = 'machine.vim'

VIM_NEXT_STATE = '`ny$@"'

VIM_TEMPLATE = """0/_v1\rnf-ly$@"

### launch with ggyy@" ###

# Init pointers
_v1-gg0mh`h/_t\rnjmt`h/_k\rnjmk`h/_o\rnjmo`h/_p\rnjmp`h/_i\rnjmi`h/_s\rnjms`h/_n:\rnjmn`h/_a\rnjma`ny$@"

_o:  # Output


_i:  # Input
100

_k:  # Current state
{initial_state}

_t:  # Current tape
{initial_tape}

_a:  # ASCII table
___0 .___1 .___2 .___3 .___4 .___5 .___6 .___7 .___8 .___9 .__10 \r_11 .__12 .__13 .__14 .__15 ._
__16 .__17 .__18 .__19 .__20 .__21 .__22 .__23 .__24 .__25 .__26 .__27 .__28 .__29 .__30 .__31 ._
__32  __33 !__34 "__35 #__36 $__37 %__38 &__39 '__40 (__41 )__42 *__43 +__44 ,__45 -__46 .__47 /_
__48 0__49 1__50 2__51 3__52 4__53 5__54 6__55 7__56 8__57 9__58 :__59 ;__60 <__61 =__62 >__63 ?_
__64 @__65 A__66 B__67 C__68 D__69 E__70 F__71 G__72 H__73 I__74 J__75 K__76 L__77 M__78 N__79 O_
__80 P__81 Q__82 R__83 S__84 T__85 U__86 V__87 W__88 X__89 Y__90 Z__91 [__92 \__93 ]__94 ^__95 __
__96 `__97 a__98 b__99 c_100 d_101 e_102 f_103 g_104 h_105 i_106 j_107 k_108 l_109 m_110 n_111 o_
_112 p_113 q_114 r_115 s_116 t_117 u_118 v_119 w_120 x_121 y_122 z_123 {{_124 |_125 }}_126 ~_127 ._
_uuu .

_n:  # Next state transition. Usage: `ny$@"
`t"tyt `ky$`s/_\V\("-t\|---\)\rf:ly$@"

_p:  # Print state. Usage: `py$@"
`ky$`op

_s:  # State transitions
{state_transitions}
# End State transitions
# Print state when unknown transition
_---: `py$@"

# vim: set whichwrap+=b,s
"""
