import sys
import os
from helpers import *

current_file = os.path.basename(__file__)
args = sys.argv

def main():
    usage_msg = f"Usage: 'python .\\{current_file} file.txt -flag\nFlags:\n-b: Outputs Machine code in binary\n-h: Outputs Machine code in hex\n-d: Outputs Machine code in decimal"
    if 2 <= len(args) <= 3:
        flag = args[2] if len(args) == 3 else "-b"
        if flag not in {"-b", "-d", "-h"}:
            waitExit(f"Invalid flag. {usage_msg}", 1)

    else:
        waitExit(f"Invalid number of arguments. {usage_msg}", 1)

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
                    out_lines = out_lines[:-1]
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

                else:
                    inst = read_inst(words)

                LC += 1
                out_lines.append(inst + "\n")
                out_lines.append(f"{bin(LC)[2:]:>012}" + "\t")

        with open("output.txt", "w") as output:
            out_lines = cnvrt(out_lines, flag)
            output.writelines(out_lines[:-1])


def cnvrt(lst, flag):
    if flag == "-b":
        return lst
    out = []
    for i in lst:
        suffix = i[-1:]
        if flag == "-d":
            out.append(str(int(i[:-1], base=2)) + suffix)
        elif flag == "-h":
            out.append(hex(int(i[:-1], base=2))[2:].upper() + suffix)
    return out


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
    suffix = 0
    if words[0] in mri:
        try:
            if words[2] == "I":
                suffix = 8
        finally:
            return mri[words[0]] + f"{bin(int(sym_table[words[1]]) + suffix)[2:]:>012}"

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