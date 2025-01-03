# Python Assembler
This python program processes a text file containing the *basic computer* assembly instructions (the one from the 70s) and generates machine code in different formats (binary, hexadecimal, or decimal). The output is saved in the same working directory in `output.txt`.

## Features
- Parses *basic computer* assembly code to generate machine code.
- Supports labels and builds a symbol-address table during the *first pass*.
- Allows output customization with multiple format flags.
- Provides detailed error messages for invalid syntax and file handling issues.
- Includes a pretty-printed symbol-address table.

## Usage
To execute the program, simply use the following command:
```bash
python <file_name> file.txt output.txt [flags]
```
Where:
- `asm.txt` is the assembly file you want to process.
- `output.txt` is the name which you want the output to be.

### Flags
- `-b`: Outputs machine code in **binary** (default).
- `-h`: Outputs machine code in **hexadecimal**.
- `-d`: Outputs machine code in **decimal**.
- `-st`: Displays the Symbolic Table in the terminal in a pretty-printed format.
---
### Example Usage
```bash
python .\main.py asm-instr.txt output.txt -h -st
```
This will
1. Generate machine code in hexadecimal format
2. Displays the symbol-address table in the terminal.

## How it works

#### 1. **First Pass**: The program scans the input file to build a **symbol-address table** for all labels defined in the assembly code.
#### 2. **Second Pass**: The program processes instructions, translates them to *machine code*, and applies the selected output format.
---

## Example Input
```bash
        ORG 100 /Origin is at memory location 100
        LDA SUB /Load 'SUB' into AC
        CME     /Complement AC
        INC     /Increment AC
        ADD MIN /ADD 'MIN' to AC
        STA DIF /Store the result in 'DIF'
        HLT     /Halt Computer
MIN,    DEC 83  /Minuend
SUB,    DEC -23 /Subtrahend
DIF,    HEX 0   /Result
        END     /End of symbolic program
```

## Example Ouput (using -h flag)
```bash
100	2107
101	7100
102	7020
103	1106
104	3108
105	7001
106	0053
107	FFE9
108	0000

```

### Dependencies
- **prettytable:** For displaying the symbolic table in a user-friendly way.
	- To install, use:
	```bash
	pip install prettytable
	```

### Project Structure
- `main.py`: The main entry point.
- `helpers.py`: Contains the instruction table necessary to translate the code (MRI and Non-MRI).

## Suggested Improvements
- Using python to run the assembly code. Outputs the variables' latest state or sth.
