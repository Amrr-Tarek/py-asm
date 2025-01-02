# Python Assembler
This python program processes a text file containing the *basic computer* assembly instructions (the one from the 70s) and generates machine code in different formats (binary, hexadecimal, or decimal). The output is saved in the same working directory in `output.txt`.

## Usage
To execute the program, simply use the following command:
```bash
python <file_name> file.txt [flags]
```
where file.txt is the assembly file you want to process
### Flags
- `-b`: Outputs machine code in **binary** (default).
- `-h`: Outputs machine code in **hexadecimal**.
- `-d`: Outputs machine code in **decimal**.
- `-st`: Prints the Symbolic Table in the terminal in a pretty-formatted way.

### Example
```bash
python .\main.py asm-instr.txt -h
```

## How it works

#### 1. **First Pass**: The program scans the file to build a **symbol-address table** for all labels defined in the assembly code.
#### 2. **Second Pass**: The program processes instructions, translates them to *machine code*, and applies the selected output format.
---
### Libraries Used
- **sys:** For managing command-line arguments.
- **os:** For getting file name for error handling.
- **prettytable:** For pretty-printing the symbolic table. To install, use:

	```bash
	pip install prettytable
	```

### Helper files
- `helpers.py`: Contains the instruction table necessary to translate the code.

## Example Input
```bash
    	ORG 100	/Origin is at memory location 100
	LDA SUB	/Load 'SUB' into AC
	CME	/Complement AC
	INC	/Increment AC
	ADD MIN	/ADD 'MIN' to AC
	STA DIF	/Store the result in 'DIF'
	HLT	/Halt Computer
MIN,	DEC 83	/Minuend
SUB,	DEC -23	/Subtrahend
DIF,	HEX 0	/Result
		END		/End of symbolic program
```

## Example Ouput (using -h flag)
```bash
0100	2107
0101	7200
0102	7020
0103	1106
0104	3108
0105	7001
0106	0053
0107	FFE9
0108	0000

```

## Suggested Improvements
- Using python to run the assembly code. Outputs the variables latest state or sth.
