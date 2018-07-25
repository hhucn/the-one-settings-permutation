import argparse
import itertools
import re
from os.path import splitext
from typing import List, Tuple

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


def generate_permutation_lists(possible_values: List[List[str]]) -> List[Tuple[str]]:
    permutations = itertools.product(*possible_values)

    return list(zip(*permutations))


def replace_possible_values_with_all_values(settings_out: str, settings_in: str, all_values: List[Tuple[str]]):
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


def split_lists_evenly(all_values: List[Tuple[str]], count: int) -> List[Tuple[str]]:
    length = len(all_values[0])
    step = length // count

    for i in range(0, length, step):
        yield [x[i:i + step] for x in all_values]


def main():
    parser = argparse.ArgumentParser(
        description="Generate settings file(s) for The ONE containing permutations of possible values")
    parser.add_argument("infile", type=str, help="Settings file to read from")
    parser.add_argument("outfile", type=str, help="Settings file to generate")
    parser.add_argument("-s", "--split", type=int, default=1, help="Split output settings permutations into x files")
    args = parser.parse_args()

    infile = args.infile
    outfile = splitext(args.outfile)
    split_count = args.split

    possible_values = read_possible_values_from_setting(infile)
    all_values = generate_permutation_lists(possible_values)

    split_lists = split_lists_evenly(all_values, split_count)

    for i in range(split_count):
        if split_count == 1:
            outfilename = "{}{}".format(*outfile)
        else:
            outfilename = "{}-{}{}".format(outfile[0], i, outfile[1])

        current_list = next(split_lists)
        list_length = len(current_list[0])
        replace_possible_values_with_all_values(outfilename, infile, current_list)
        print("Generated {out} with {length} combinations: ./one.sh -b {length} {out}".format(out=outfilename,
                                                                                              length=list_length))


if __name__ == "__main__":
    main()
