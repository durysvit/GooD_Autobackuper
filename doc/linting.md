# Linting

Popular static analysis tools were selected:
* Flake8;
* Mypy;
* Pylint;
* Bandit.

# About

The tools are configured by default, but the following rules have been added to follow the camelCase style (add to VSCode settings):

```
"pylint.args": ["--method-rgx=^[a-z][a-zA-Z0-9]+$"]
"pylint.args": ["--function-rgx=^[a-z][a-zA-Z0-9]+$"]
"pylint.args": ["--argument-rgx=^[a-z][a-zA-Z0-9]+$"]
"pylint.args": ["--variable-rgx=^[a-z][a-zA-Z0-9]+$"]
"pylint.args": ["--attr-rgx=^[a-z][a-zA-Z0-9]+$"]
```

and see [docs.pylint](https://docs.pylint.org/).

# Installation

## VSCode

In VSCode install:
* [Flake8](https://open-vsx.org/vscode/item?itemName=ms-python.flake8);
* [Mypy](https://open-vsx.org/vscode/item?itemName=ms-python.mypy-type-checker);
* [Pylint](https://open-vsx.org/vscode/item?itemName=ms-python.pylint).

## Pip

Or install via Pip:

```
python -m venv venv
. ./venv/bin/activate
pip install flake8 pylint mypy bandit
```

Run (e.g.):

```
pylint <fileName>.py
flake8 <fileName>.py
mypy <fileName>.py
bandit -r . -f html -o bandit_report.html
```
