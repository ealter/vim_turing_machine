Vim Turing Machine
==================

Ever wish you could run your code in your editor? Tired of installing huge
dependencies like bash or python to run your scripts? Love Vim so much that you
never want to leave it? Why not run your code... in your editor itself? Enter
vim_turing_machine: a tool to allow you to run a Turing machine using only
normal mode Vim commands.

And now you might ask, but what can we do on a Turing machine! To demonstrate
its capabilities, we implemented a solution to the Merge Overlapping Intervals
question and defined all the state transitions needed to solve this
glorious problem. So next time you need to merge some intervals, don't
hand-write a 10-line python program. Instead, take out your favorite editor and
watch it solve the problem in less than a minute with 1400 state transitions!

But a simple naysayer may say, 'We already have vimscript! Why in God's name
would I want to use a Turing machine instead?' To that, we retort: our Turing
machine only uses normal mode. So you could theoretically just type in the
program and then execute it without running a single script! No ex mode either!
This project proves that normal mode in Vim is as powerful as any computer!

Merging your favorite intervals
===============================

Given a set of sorted potentially overlapping open/close intervals, merge the
overlapping intervals together.

Example:
```
[[1, 5], [6, 7]] -> [[1, 5], [6, 7]]
[[1, 5], [2, 3], [5, 7], [12, 15]] -> [[1, 7], [12, 15]]
```

Running the Python Turing Machine: `make run`

Opening the Vim Turing Machine without running it: `make open-vim-machine`

Opening and then running the Vim Turing Machine: `make run-vim-machine`

So Vim did what? Wait. How does it even?
========================================

So you run this program, and it works. Great! So what happened? Well the most
common thing you're going to see is `y$@"`. What this does is yank from the
current cursor to the end of the line and then executes the default register as
a macro. This allows us to encode motions in lines and then execute them. We
then chain lines together by ending lines with moving to a mark, or a search
result, and then yanking and executing that line.

Using that nifty trick, we begin by yanking the first line and executing it.
That then sets off our mark initialization. We then search for `_<someletter>`
and then mark that position with the corresponding letter. Generally the first
initial of whatever the thing we're marking is. Once everything is marked, we
then begin the state transitions.

We begin a state transition by executing a long command (located at `_n:`)
which jumps to the tape marker, yanks it, then jumps to the current state
marker, yanks that too, and then searches for some transition that contains both
the state and tape values. Once it gets to that line, it jumps to the command
string and then executes our trusty `y$@"` to execute it. To make sure we keep
transitioning, each state transition ends with `` `ny$@ `` which tells it to jump
to our "next state" marker and then execute it again, which kicks off the search
for the next state.

The execution halts when it can't find a new state to transition to. The state
search includes an "or" operator where it will fall back to matching `---`,
which tells it to print the current state and halt.

Most transitions themselves involve changing a tape value or a state value and
then moving in some direction on the tape. Changing values consists of jumping
to the tape or state marks (`` `t `` or `` `k `` respectively) and then using
`cw` or `C` to change the value. We then move the pointer by jumping to the tape
position (`` `t ``) and then moving a word forward (`W`) or backward (`B`), and
then marking the new tape position.

The last real piece of complication is extending the tape. We're living in a
world with unlimited tapes! What a time to be alive! This is done through a
series of nifty hacks. First, we have a modeline that sets `whichwrap+b,s`. This
allows us to move across line breaks and keep the tape all in the screen. Next,
the line directly under the tape contains a "fake" value that, when added to our
state search, will prevent it from matching any real state transitions and
instead match a "transition" for adding a line to the tape. This line tells us
to jump to the end of the tape, and then insert a full line of empty values (we
use `X`), and then go back to our original tape location and execute the next
state transition!

And there you have it! A simple `ggyy@"` will kick off all of these sequences
until execution completes. The cool thing is that this isn't special to the
intervals problem. In fact, you can write your own state machine and use the
provided Vim adapter to create a new Vim machine to solve any problem that can
be solved by a Turing Machine!

To see some more details about various common commands, you can take a look at
`vim_turing_machine/vim_constants.py`. That file contains some constants that
are used repeatedly in the generated `machine.vim` file and their names are
fairly descriptive. Also, if you'd like to step through manually, you can edit
the Vim machine in `vim_turing_machine/machines/vim_is_number_even.py` and tell
it not to auto step and then step through manually using `y$@"`.

Happy hacking!

Dependencies
============

To run this code, you will need `python3.6`, `tox`, and `vim` installed on your
machine. This code hasn't been tested on other versions of python3, but they'll
probably work if you change the pinned version in `tox.ini`. This code is not
python2 compatible.

Contributors
============

eliot and ifij wrote this project in July 2017 for Yelp's Hackathon 23. It was inspired by [vimmmex](https://github.com/xoreaxeaxeax/vimmmex): a Brainfuck interpretor written in Vim.

[modeline]: # ( vim: set fenc=utf-8 spell spl=en textwidth=80: )
