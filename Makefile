#!/bin/bash

# Setting
SHELL := /bin/bash
.DEFAULT_GOAL := info

# Component
.PHONY: venv

venv:
	python -m venv venv --upgrade-deps

install:
	venv/Scripts/pip install -r requirements.txt

run:
	python guess_wordle.py --size 5 --seed 1234

info:
	@echo -e "====================================================================================="
	@echo -e "Application:\t\t\e[34mProject > Wordle Puzzle Solution\e[0m"
	@cat project.yaml | grep description | awk "{ print $2 }"
	@cat project.yaml | grep version | awk "{ print $2 }"
	@cat project.yaml | grep revision | awk "{ print $2 }"
	@echo -e "====================================================================================="
	@echo -e ""
	@echo -e "> Supported target =================================================================="
	@echo -e "make info: \t\tGet information about the project"
	@echo -e "make install: \t\tInstall development dependencies"
	@echo -e "make run: \t\tRun the application"
	@echo -e ""
