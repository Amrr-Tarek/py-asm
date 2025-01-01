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
        sym_table = first_pass(args[1])
        print(sym_table)
        
        # second pass

    except FileNotFoundError:
        print(f"'{args[1]}' Not Found!")

    else:
        pass


def waitExit(msg, code):
    print(msg)
    print("Press Enter to terminate..")
    input()
    exit(code)


def first_pass(file) -> dict[str, int]:
    table = {}
    LC = 0
    with open(file, "r") as file:
        for line in file:  # reads a line
            words = line.upper().split()
            if words[0] == 'ORG':
                LC = int(words[1])
                continue
                ############################
            elif words[0].endswith(','):
                table[words[0][:-1]] = LC
            elif words[0] == 'END':
                return table
            LC += 1
            
    return table


if __name__ == "__main__":
    main()