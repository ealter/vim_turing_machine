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
watch it solve the problem in less than a minute with 1500 state transitions!

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
[[1, 5], [6, 7]] -> [[1, 5], [6, 7]]
[[1, 5], [2, 3], [5, 7], [12, 15]] -> [[1, 7], [12, 15]]

To run this problem on a python Turing machine, just call `make run`. To run
this problem on a Vim Turing machine, just call `make run-vim-machine`. To see
the Vim Turing machine without running it, call `make open-vim-machine`.

Contributors
============

eliot and ifij wrote this project in July 2017 for Yelp's Hackathon 23.
