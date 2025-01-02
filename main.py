import sys
import os
from prettytable import PrettyTable
from helpers import *


def main(args: list[str], current_file: str) -> None:
    output_name = ""
    usage_msg = f"""Usage: 'python .\\{current_file} asm.txt output.txt [flags]
    Flags:
    -b: Outputs Machine code in binary
    -h: Outputs Machine code in hex
    -d: Outputs Machine code in decimal
    -st: Prints the symbolic table in the terminal"""
    if not 2 <= len(args) <= 5:
        Exit(f"Invalid number of arguments. {usage_msg}", 2)

    flag = "-b"
    show_sym_table = False
    output_name = "output.txt"

    if len(args) >= 3 and not args[2].startswith("-"):
        output_name = args[2]
        args = [args[0], args[1]] + args[3:]

    for arg in args[2:]:
        if arg in {"-b", "-d", "-h"}:
            flag = arg
        elif arg == "-st":
            show_sym_table = True
        else:
            Exit(f"Invalid flag. {usage_msg}", 1)

    try:
        sym_table = first_pass(args[1])
        print_sym_table(sym_table) if show_sym_table else None

    except FileNotFoundError:
        Exit(f"ERROR: File '{args[1]}' Not Found!", 7)

    out_lines = process_file(args[1], flag, sym_table)
    with open(output_name, "w") as output:
        out_lines = convert(out_lines, flag)
        output.writelines(out_lines[:-1])


def process_file(file_path: str, flag: str, sym_table: dict[str, int]) -> None:
    """
    Performs the second pass, processes the input file, outputs the result in output.txt in the same directory
    """
    LC = 0x0
    out_lines = []
    with open(file_path) as file:
        ln = 0
        for line in file:  # reads a line
            ln += 1
            words = line.upper().split()
            for i, word in enumerate(words):
                if word.startswith("/"):
                    words = words[:i]
                    break

            if not words:
                continue

            if words[0].startswith("/"):
                print(line)
                print(words)

            if words[0] == "END":
                break

            elif words[0] == "ORG":
                LC = int(words[1], base=16)

                out_lines = out_lines[:-1]
                out_lines.append(f"{bin(LC)[2:]:>012}" + "\t")
                continue

            elif words[0].endswith(","):  # if label
                inst = read_inst(words[1:], sym_table, ln)

            else:  # if normal instruction
                inst = read_inst(words, sym_table, ln)

            LC += 1
            out_lines.append(inst + "\n")
            out_lines.append(f"{bin(LC)[2:]:>012}" + "\t")

    return out_lines


def read_inst(words: list, table: dict, line_number) -> str:
    """
    Reads and parses an instruction line, returning its binary representation
    """
    try:
        if words[0] in mri:
            suffix = 8 if len(words) > 2 and words[2] == "I" else 0
            return f"{bin(int(mri[words[0]], base=2) + suffix)[2:]:>04}" + str_to_bin(
                table[words[1]], 16, 12
            )  #

        if words[0] in non_mri:
            return str_to_bin(non_mri[words[0]], 16)

        if words[0] == "DEC":
            return str_to_bin(words[1])

        if words[0] == "HEX":
            return str_to_bin(words[1], 16)

    except Exception as e:
        Exit(f"Invalid Syntax on line {line_number}.\nError: {e}", 4)

    else:
        Exit(
            f"Invalid Syntax on line {line_number}.\nInvalid Instruction '{words[0]}'",
            5,
        )


def convert(lst: list[str], flag: str, size: int = 4) -> list:
    """
    Converts the machine code to specific format (binary, decimal, hexdecimal). Controlled by the flag.
    """
    if flag == "-b":
        return lst
    out = []
    for i in lst:
        suffix = i[-1:]
        if flag == "-d":
            res = str(int(i[:-1], base=2))
        elif flag == "-h":
            if suffix == "\t":
                size = 3
            elif suffix == "\n":
                size = 4
            res = hex(int(i[:-1], base=2))[2:].zfill(size).upper()
        out.append(res + suffix)
    return out


def str_to_bin(txt: str, base=10, size: int = 16) -> str:
    """
    Converts numbers to binary
    """
    return bin(0xFFFF & int(str(txt), base=base))[2:].zfill(size)


def first_pass(file: str) -> dict[int, str]:
    """
    Performs the first pass.
    Returns the symbol address table for the labels
    """
    table = {}
    LC = 0x0
    with open(file, "r") as f:
        lc = 0
        for line in f:  # reads a line
            lc += 1
            words = line.upper().split()

            if not words or words[0].startswith("/"):
                continue

            if words[0] == "ORG":
                try:
                    LC = int(words[1], 16)
                except ValueError:
                    Exit(f"Invalid Syntax on line {lc}. => '{words[1]}'", 3)
                continue

            elif words[0].endswith(","):  # if a label
                if len(words[0]) > 4:
                    Exit(
                        f"Invalid label length at line: {lc}!\nOnly 3 characters long labels are allowed",
                        6,
                    )
                table[words[0][:-1]] = hex(LC)[2:].upper()

            elif words[0] == "END":
                return table
            LC += 1

    return table


def Exit(msg: str, code: int) -> None:
    """
    Prints an error message followed by waiting for user to press enter.
    """
    print(msg)
    exit(code)


def print_sym_table(sym_table: dict) -> None:
    table = PrettyTable()
    table.field_names = ["Label", "Address (Hex)"]

    for label, address in sym_table.items():
        table.add_row([label, address])

    print(table)


if __name__ == "__main__":
    current_file = os.path.basename(__file__)
    args = sys.argv
    main(args, current_file)
