#!/bin/bash

venv:
	python -m venv venv --upgrade-deps

install:
	venv/Scripts/pip install -r requirements.txt

run:
	python guess_wordle.py --size 5 --seed 1234
