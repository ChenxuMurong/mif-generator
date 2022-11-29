# MIF-generator
A mini-assembler that generates MIF files from a much more readable syntax. Extention for CS 232 Project 7 (RISC CPU)

## Usage: 

`python3 mif_generator.py [> ...]`

The output will be the text content of a .mif file, with meta information that works with the CPU.

The program prints to stdout by default but you can use the pipe function ">" to make it print to a certain output file.


## Syntax:

```MOVE [from {SRC} / {bits}] to {dest}
ADD/SUB/XOR/AND/OR {srcA} to/from/with {srcB} -> {dest}
SHIFT/ROTATE {src} left/right -> {dest}
BRANCH [to] {addr} (addr is in 1-based decimal)
BRANCH [to] {addr} if zero/overflow/negative/carry (addr is in 1-based decimal)

LOAD from {addr} to {dest} [indexed] (addr is 1-based decimal)
STORE from {src} to {addr} [indexed] (addr is 1-based decimal)

CALL {addr}
RETURN

OPORT {src}
IPORT {dest}

EXIT
```
Comments must be preceded by `" # "` where both white spaces are mandatory.

Every line must have code. No empty lines or lines that contain comment only are allowed.
