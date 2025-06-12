# Docstrings

## Installation

Install [pdoc](https://pdoc.dev/docs/pdoc.html) via Pip:

```
pip install pdoc
```

## Convention 

Documentation comments should be written like this:

```
"""
Desctiption.

Args:
    name (type): Description.
    <...>

Returns:
    type: Description.
    <...>

Raises:
    ExceptionName: raise if <...>
"""
```

Run (e.g.):

```
PYTHONPATH=. pdoc main app const exception script view worker controller model service logger util -o ./doc/code --favicon ../../GooD_Autobackuper.svg
```
