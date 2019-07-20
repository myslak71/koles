# koles

[![Build Status](https://travis-ci.com/myslak71/koles.svg?token=s1Zd7YYn4fqxstysFsVc&branch=master)](https://travis-ci.com/myslak71/koles)
![image](https://img.shields.io/badge/python-3.7-blue.svg)

Watch your language young pal!

Inaccessible files are omitted.

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
