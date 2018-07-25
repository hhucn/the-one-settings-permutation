import argparse
import itertools
import re
from typing import List, Iterable


MULTIPLE_VALUES_SETTING_REGEX = r"^[^#][^=]* = \[([^\]]+)\]"
MULTIPLE_VALUES_SUB_REGEX = r"\[[^\]]+\]"


def read_possible_values_from_setting(settingsfile: str) -> List[List[str]]:
    possible_values = []

    with open(settingsfile, "r") as f:
        matcher = re.compile(MULTIPLE_VALUES_SETTING_REGEX)

        for line in f:
            match = matcher.match(line)

            if match:
                possible_values.append(match.group(1).split(";"))

    return possible_values


def generate_permutation_lists(possible_values: List[List[str]]) -> List[Iterable[str]]:
    permutations = itertools.product(*possible_values)

    return list(zip(*permutations))


def replace_possible_values_with_all_values(settings_out: str, settings_in: str, all_values: List[Iterable[str]]):
    matcher = re.compile(MULTIPLE_VALUES_SETTING_REGEX)
    replacer = re.compile(MULTIPLE_VALUES_SUB_REGEX)
    value_index = 0

    with open(settings_out, "w") as outfile, open(settings_in, "r") as infile:
        for line in infile:
            if matcher.match(line):
                value_line = "[{}]".format(";".join(all_values[value_index]))
                value_index += 1

                line = replacer.sub(value_line, line)

            outfile.write(line)


def main():
    parser = argparse.ArgumentParser(
        description="Generate settings file(s) for The ONE containing permutations of possible values")
    parser.add_argument("infile", type=str, help="Settings file to read from")
    parser.add_argument("outfile", type=str, help="Settings file to generate")
    parser.add_argument("-s", "--split", type=int, help="Split output settings permutations into x files")
    args = parser.parse_args()

    infile = args.infile
    outfile = args.outfile
    split_count = args.split

    possible_values = read_possible_values_from_setting(infile)
    print(possible_values)
    all_values = generate_permutation_lists(possible_values)
    print(all_values)
    replace_possible_values_with_all_values(outfile, infile, all_values)


if __name__ == "__main__":
    main()
