.PHONY: minimal
minimal: venv

venv:
	tox -e venv

.PHONY: test
test:
	tox

.PHONY: clean
clean:
	find . -name '*.pyc' -delete
	find . -name '__pycache__' -delete
	rm -rf .tox
	rm -rf venv
	rm machine.vim

.PHONY: run-vim
run-vim: venv
	venv/bin/python -m vim_turing_machine.machines.vim_is_number_even 10

open-vim-machine: run-vim
	vim -u vimrc machine.vim
