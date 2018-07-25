# Permutate Settings for the ONE

The ONE's batch mode expects multiple values for different scenario runs in one
batch, but doesn't offer any method to create permutations from possible
setting values.
This tool creates all possible permutations (the cross-product of all
value vectors) and outputs them in one file or across multiple files evenly.

Multiple files can be helpful if you plan running multiple simulator instances
in parallel, each using its own settings file.

To help understand its function, the following example is given:

##### Example
Example settings:
```
setting1 = [1;2]
setting2 = [a;b]
```

###### Example of the ONE's behavior
Result: `1a` and `2b`.

###### Example of the permutation behavior
Result: `1a`, `1b`, `2a` and `2b`



## Setup
As only modules from the Python Standard Library are used, a recent Python 3
installation is sufficient.
To use it in a virtual environment, `pipenv` is preferred:
```bash
$ pipenv install
```

## Usage

```bash
$ pipenv run python permutator/permutator.py default_settings.txt test.txt
Generated test.txt with 12 combinations: ./one.sh -b 12 test.txt
```

```bash
$ pipenv run python permutator/permutator.py -s 2 default_settings.txt test.txt
Generated test-0.txt with 6 combinations: ./one.sh -b 6 test-0.txt
Generated test-1.txt with 6 combinations: ./one.sh -b 6 test-1.txt
```

## Help
```bash
$ pipenv run python permutator/permutator.py -h
usage: permutator.py [-h] [-s SPLIT] infile outfile

Generate settings file(s) for The ONE containing permutations of possible
values

positional arguments:
  infile                Settings file to read from
  outfile               Settings file to generate

optional arguments:
  -h, --help            show this help message and exit
  -s SPLIT, --split SPLIT
                        Split output settings permutations into x files
```