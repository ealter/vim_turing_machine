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
build-vim: venv
	venv/bin/python -m vim_turing_machine.machines.vim_is_number_even 11

open-vim-machine: build-vim
	vim -u vimrc machine.vim

run-vim-machine: build-vim
	vim -u vimrc machine.vim -c ':normal gg0yy@"'
