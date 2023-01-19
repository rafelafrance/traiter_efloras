.PHONY: test install dev venv clean
.ONESHELL:

VENV=.venv
PYTHON=./$(VENV)/bin/python3.10

test:
	$(PYTHON) -m unittest discover

install: venv
	source $(VENV)/bin/activate
	$(PYTHON) -m pip install -U pip setuptools wheel
	$(PYTHON) -m pip install .
	$(PYTHON) -m pip install git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
	$(PYTHON) -m pip install git+https://github.com/rafelafrance/traiterplants.git@master#egg=traiterplants
	$(PYTHON) -m spacy download en_core_web_sm

dev: venv
	source $(VENV)/bin/activate
	$(PYTHON) -m pip install -U pip setuptools wheel
	$(PYTHON) -m pip install -e .[dev]
	$(PYTHON) -m pip install -e ../traiter
	$(PYTHON) -m pip install -e ../traiterplants
	$(PYTHON) -m spacy download en_core_web_sm
	pre-commit install

venv:
	test -d $(VENV) || python3.10 -m venv $(VENV)

clean:
	rm -r $(VENV)
	find -iname "*.pyc" -delete
