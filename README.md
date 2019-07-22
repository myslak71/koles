# koles

[![Build Status](https://travis-ci.org/myslak71/koles.svg?branch=develop)](https://travis-ci.org/myslak71/koles)
[![Coverage Status](https://coveralls.io/repos/github/myslak71/koles/badge.svg?branch=develop)](https://coveralls.io/github/myslak71/koles?branch=develop)
![image](https://img.shields.io/badge/python-3.7-blue.svg)


Watch your language young pal!

Inaccessible files or files without proper decoding are omitted.

## Installation
```
pip install git+https://github.com/myslak71/koles.git
```

## Usage
```
koles <path>
```

## Example
```
koles .
```

### Output

```
./koles/checker.py:29: Inappropriate vocabulary found at positions: [65]
./koles/checker.py:32: Inappropriate vocabulary found at positions: [41]
./koles/checker.py:33: Inappropriate vocabulary found at positions: [21]
./koles/checker.py:35: Inappropriate vocabulary found at positions: [56]
./koles/checker.py:39: Inappropriate vocabulary found at positions: [41, 57]
./koles/checker.py:40: Inappropriate vocabulary found at positions: [66]
./koles/checker.py:58: Inappropriate vocabulary found at positions: [40]
```

## Development notes
`make lint` - runs all linters

`make flake8` - runs flake8

`make unittests` - runs unittests with coverage report and -s flag

`make mypy` - runs mypy

`make yamllint` - runs yamllint
