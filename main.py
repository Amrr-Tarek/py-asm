import sys
import os
from pathlib import Path
from helpers import *

current_file = Path(__file__)

args = sys.argv


def main():
    if len(args) != 2:
        waitExit(f"Usage: 'python .\\{current_file.name} file.txt", 1)

    try:
        global sym_table
        sym_table = first_pass(args[1])
        print(sym_table)

    except FileNotFoundError:
        print(f"'{args[1]}' Not Found!")

    else:
        # second pass
        LC = 0
        out_lines = []
        with open(args[1]) as file:
            for line in file:  # reads a line
                words = line.upper().split()
                if words[0] == "END":
                    break

                elif words[0] == "ORG":
                    LC = int(words[1])
                    out_lines.append(f"{bin(LC)[2:]:>012}" + "\t")
                    ##################
                    continue

                elif words[0].endswith(","):  # if label
                    if words[1] == "DEC":
                        inst = str_to_bin(words[2])
                    elif words[1] == "HEX":
                        inst = str_to_bin(words[2], 16)
                    else:
                        inst = read_inst(words[1:])
                    print(f"LC: {LC} INST: {inst}")

                else:
                    inst = read_inst(words)
                    print(f"LC: {LC} INST: {inst}")

                LC += 1
                out_lines.append(inst + "\n")
                out_lines.append(f"{bin(LC)[2:]:>012}" + "\t")

        with open("output.txt", "w") as output:
            output.writelines(out_lines[:-1])


def first_pass(file) -> dict[int, str]:  # remember to output a binary or hex for debug
    table = {}
    LC = 0
    with open(file, "r") as file:
        for line in file:  # reads a line
            words = line.upper().split()
            if words[0] == "ORG":
                LC = int(words[1])
                ############################
                continue

            elif words[0].endswith(","):  # if a label
                table[words[0][:-1]] = LC

            elif words[0] == "END":
                return table
            LC += 1

    return table


def read_inst(words) -> str:
    if words[0] in mri:
        return mri[words[0]] + f"{bin(int(sym_table[words[1]]))[2:]:>012}"

    if words[0] in non_mri:
        return str_to_bin(non_mri[words[0]], 16)


def str_to_bin(txt, base=10):
    return f"{bin(0xFFFF & int(str(txt), base=base))[2:]:>016}"


def waitExit(msg, code):
    print(msg)
    print("Press Enter to terminate..")
    input()
    exit(code)


if __name__ == "__main__":
    main()
    stri = str_to_bin(-23, 10)
