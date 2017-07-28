.PHONY: minimal
minimal: venv

venv:
	tox -e venv

.PHONY: install-hooks
install-hooks: venv
	venv/bin/pre-commit install-hooks
	venv/bin/pre-commit install

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

.PHONY: run
run: venv
	venv/bin/python -m vim_turing_machine.machines.merge_business_hours.merge_business_hours '[[1,2],[2,3],[5,8]]' 5

.PHONY: run-vim
build-vim: venv
	venv/bin/python -m vim_turing_machine.machines.merge_business_hours.vim_merge_business_hours '[[1,2],[2,3],[5,8]]' 5

open-vim-machine: build-vim
	vim -u vimrc machine.vim

run-vim-machine: build-vim
	vim -u vimrc machine.vim -c ':normal gg0yy@"'
