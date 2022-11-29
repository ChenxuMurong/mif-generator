'''
Author Jue Wang
Assembler that translates English to 16-bit mif code for CS232 Proj 7 (CPU)
Searches for a file named "instructions.txt" as input

Usage: 

python3 mif_generator.py [> ...]

The output will be the text content of a .mif file, with meta information that works with the CPU.

The program prints to stdout by default but you can use the pipe function ">" to make it print to a certain output file.


Syntax:

MOVE [from {SRC} / {bits}] to {dest}
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

comments must be preceded by " -- " both white spaces are mandatory

every line must have code. No empty lines or comment lines are allowed
'''


def raiseError(message):
    print(f"error: {message}")
    exit()


def translate(line):
    # case insensitive
    line = line.lower()
    words = line.split(' ')

    op = words[0]
    ans = ""

    if op == "move":
        '''syntax: 
        move [[from] [acc/lr] / [bits]] to [dest] '''
        # check how many words are in here
        if len(words) > 5 or len(words) < 4:
            raiseError("wrong number of args. check syntax in move.")
        
        ans += "1111"
        vals = "00000" # unused filler bits

        src = words[1]
        if words[1] == "from":
            src = words[2]
        # TABLE D
        if src == "ra":
            ans += "0000"
        elif src == "rb":
            ans += "0001"
        elif src == "rc":
            ans += "0010"
        elif src == "rd":
            ans += "0011"
        elif src == "re":
            ans += "0100"
        elif src == "sp":
            ans += "0101"
        elif src == "pc":
            ans += "0110"
        elif src == "ir":
            ans += "0111"
        elif src.isnumeric():
            ans += "1"
            src_bits = '{0:0>8b}'.format(int(src))
            vals = src_bits
        else:
            raiseError(f"invalid source {src} in move")

        ans += vals

        # TABLE B
        if words[-1] == "ra":
            ans += "000"
        elif words[-1] == "rb":
            ans += "001"
        elif words[-1] == "rc":
            ans += "010"
        elif words[-1] == "rd":
            ans += "011"
        elif words[-1] == "re":
            ans += "100"
        elif words[-1] == "sp":
            ans += "101"
        else: 
            raiseError(f"invalid destination {words[-1]} in move")
        
        return ans        
    # bin arith
    elif op == "add" or op == "sub" or op == "xor" or op == "and" or op == "or":
        '''bin syntax:
            [add/sub/xor/and/or] {srcA} [to/from/with] {srcB} -> {dest}'''
        if len(words) != 6:
            raiseError("wrong number of args. check syntax in bin.")
    
        ans += "1"

        operation = words[0]
        srcA = words[1]
        srcB = words[3]
        dest = words[5]

        if operation == "add":
            ans += "000"
        elif operation == "sub":
            ans += "001"
        elif operation == "and":
            ans += "010"
        elif operation == "or":
            ans += "011"
        elif operation == "xor":
            ans += "100"
        else: 
            raiseError(f"invalid operation {words[1]} in bin")
        
        # table E
        if srcA == "ra":
            ans += "000"
        elif srcA == "rb":
            ans += "001"
        elif srcA == "rc":
            ans += "010"
        elif srcA == "rd":
            ans += "011"
        elif srcA == "re":
            ans += "100"
        elif srcA == "sp":
            ans += "101"
        elif srcA == "all0s":
            ans += "110"
        elif srcA == "all1s":
            ans += "111"
        else:
            raiseError(f"invalid source A {srcA} in binary arithmetics")

        # table E
        if srcB == "ra":
            ans += "000"
        elif srcB == "rb":
            ans += "001"
        elif srcB == "rc":
            ans += "010"
        elif srcB == "rd":
            ans += "011"
        elif srcB == "re":
            ans += "100"
        elif srcB == "sp":
            ans += "101"
        elif srcB == "all0s":
            ans += "110"
        elif srcB == "all1s":
            ans += "111"
        else:
            raiseError(f"invalid source B {srcB} in bin")
        
        ans += "000"

        # TABLE B
        if dest == "ra":
            ans += "000"
        elif dest == "rb":
            ans += "001"
        elif dest == "rc":
            ans += "010"
        elif dest == "rd":
            ans += "011"
        elif dest == "re":
            ans += "100"
        elif dest == "sp":
            ans += "101"
        else: 
            raiseError(f"invalid destination {dest} in binary arithmetic")
        
        return ans

    elif op == "shift" or op == "rotate":
        '''
        shift/rotate {src} left/right -> {dest}
        '''
        src = words[1]
        direction = words[2]
        dest = words[4]
        ans = "1"

        if op == "shift":
            ans += "101"
            if direction == "left":
                ans += "0"
            elif direction == "right":
                ans += "1"
            else:
                raiseError(f"Undefined direction {direction} with op {op}")
        elif op == "rotate":
            ans += "110"
            if direction == "left":
                ans += "0"
            elif direction == "right":
                ans += "1"
            else:
                raiseError(f"Undefined direction {direction} with op {op}")
        
        # table E
        if src == "ra":
            ans += "000"
        elif src == "rb":
            ans += "001"
        elif src == "rc":
            ans += "010"
        elif src == "rd":
            ans += "011"
        elif src == "re":
            ans += "100"
        elif src == "sp":
            ans += "101"
        elif src == "all0s":
            ans += "110"
        elif src == "all1s":
            ans += "111"
        else:
            raiseError(f"invalid source A {src} in binary arithmetics")
        
        ans += "000"

        # TABLE B
        if dest == "ra":
            ans += "000"
        elif dest == "rb":
            ans += "001"
        elif dest == "rc":
            ans += "010"
        elif dest == "rd":
            ans += "011"
        elif dest == "re":
            ans += "100"
        elif dest == "sp":
            ans += "101"
        else: 
            raiseError(f"invalid destination {dest} in move")
        
        return ans
    
    elif op == "branch":
        '''branch syntax (address is in 1-based decimal)
        branch [to] {addr}
        branch [to] {addr} if zero/overflow/negative/carry'''
        # branch or conditional branch
        ans += "001"

        addr = words[1]
        if words[1] == "to":
            addr = words[2]
        
        addr = '{0:0>8b}'.format(int(addr) - 1)
            
        for dig in addr:
            if dig != '0' and dig != '1':
                raiseError(f"invalid address {addr} in branch")

        if "if" in words:
            ans += "100" # conditional branching

            # word after if
            idx = words.index("if")
            cond = words[idx + 1]

            if cond == "zero":
                ans += "00"
            elif cond == "overflow":
                ans += "01"
            elif cond == "negative":
                ans += "10"
            elif cond == "carry":
                ans += "11"
            else:
                raiseError(f"invalid condition {cond} in conditional branch")

            ans += addr

        else:
            ans += "00000" # 0 for unconditional branch, the rest for padding
            ans += addr

        return ans

    elif op == "load":
        '''LOAD from {addr} to {dest} [indexed]'''

        addr = words[2]
        dest = words[4]
        isIndexed = len(words) == 6        
        
        ans += "0000"
        ans += str(int(isIndexed)) # 0 or 1
        
        # TABLE B
        if dest == "ra":
            ans += "000"
        elif dest == "rb":
            ans += "001"
        elif dest == "rc":
            ans += "010"
        elif dest == "rd":
            ans += "011"
        elif dest == "re":
            ans += "100"
        elif dest == "sp":
            ans += "101"
        else: 
            raiseError(f"invalid destination {dest} in load")

        ans += '{0:0>8b}'.format(int(addr) - 1)
        return ans
        
    elif op == "store":
        '''STORE from {src} to {addr} [indexed] (addr is 1-based decimal)'''

        src = words[2]
        addr = words[4]
        isIndexed = len(words) == 6
        
        ans += "0001"
        ans += str(int(isIndexed)) # 0 or 1
        
        # TABLE B
        if src == "ra":
            ans += "000"
        elif src == "rb":
            ans += "001"
        elif src == "rc":
            ans += "010"
        elif src == "rd":
            ans += "011"
        elif src == "re":
            ans += "100"
        elif src == "sp":
            ans += "101"
        else: 
            raiseError(f"invalid source {src} in store")

        ans += '{0:0>8b}'.format(int(addr) - 1)
        return ans

    elif op == "call":
        '''CALL {addr}'''
        addr = words[-1]
        addr = '{0:0>8b}'.format(int(addr) - 1)
        ans += "00110100"

        ans += addr
        return ans

    elif op == "return":
        return "0011100000000000"

    elif op == "exit":
        return "0011110000000000"
    
    elif op == "push":
        '''PUSH {src}'''
        src = words[-1]
        ans += "0100"

        # TABLE D
        if src == "ra":
            ans += "000"
        elif src == "rb":
            ans += "001"
        elif src == "rc":
            ans += "010"
        elif src == "rd":
            ans += "011"
        elif src == "re":
            ans += "100"
        elif src == "sp":
            ans += "101"
        elif src == "pc":
            ans += "110"
        elif src == "cr":
            ans += "111"
        else:
            raiseError(f"invalid source {src} in move")

        ans += "000000000"

        return ans
   
    elif op == "pop":
        '''POP {src}'''
        src = words[-1]
        ans += "0101"

        # TABLE D
        if src == "ra":
            ans += "000"
        elif src == "rb":
            ans += "001"
        elif src == "rc":
            ans += "010"
        elif src == "rd":
            ans += "011"
        elif src == "re":
            ans += "100"
        elif src == "sp":
            ans += "101"
        elif src == "pc":
            ans += "110"
        elif src == "cr":
            ans += "111"
        else:
            raiseError(f"invalid source {src} in move")

        ans += "000000000"

        return ans
        
    elif op == "oport":
        '''OPORT {src}'''
        
        ans += "0110"
        src = words[-1]
        
        # TABLE D
        if src == "ra":
            ans += "000"
        elif src == "rb":
            ans += "001"
        elif src == "rc":
            ans += "010"
        elif src == "rd":
            ans += "011"
        elif src == "re":
            ans += "100"
        elif src == "sp":
            ans += "101"
        elif src == "pc":
            ans += "110"
        elif src == "cr":
            ans += "111"
        else:
            raiseError(f"invalid source {src} in move")

        ans += "000000000"
        return ans
    
    elif op == "iport":
        '''IPORT {dest}'''

        ans += "0111"

        # TABLE B
        if words[-1] == "ra":
            ans += "000"
        elif words[-1] == "rb":
            ans += "001"
        elif words[-1] == "rc":
            ans += "010"
        elif words[-1] == "rd":
            ans += "011"
        elif words[-1] == "re":
            ans += "100"
        elif words[-1] == "sp":
            ans += "101"
        else: 
            raiseError(f"invalid destination {words[-1]} in iport")
        
        ans += "000000000"
        return ans
    

    else:
        raiseError(f"invalid op {op}")


def main():
    with open("instructions.txt") as file:
        meta = '''-- program memory file for instructions.a
DEPTH = 256;
WIDTH = 16;
ADDRESS_RADIX = HEX;
DATA_RADIX = BIN;
CONTENT
BEGIN\n'''
        # first line
        line = file.readline().strip()
        for i,char in enumerate(line):
            if char == '#':
                line = line[:i].strip()
                break

        code = meta
        lineNum = 0
        while len(line) != 0:
            # line number is two-digit hex
            code +=  "{0:0>2X} : {1};".format(lineNum, translate(line))
            # add English annotation to code
            code += " -- " + line + "\n"

            # read next line
            line = file.readline().strip()
            for i,char in enumerate(line):
                if char == '#':
                    line = line[:i].strip()
                    break

            lineNum += 1
        if lineNum < 255:
            code += "[{0:0>2X}..FF] : 1111111111111111;\n".format(lineNum)
        code += "END"
        print(code)


if __name__ == "__main__":
    main()
