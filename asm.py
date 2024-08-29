import re

# Define opcode mappings
opcodes = {
    "LDA": "0001",
    "STA": "0010",
    "ADD": "0011",
    "SUB": "0100",
    "LDI": "0101",
    "JMP": "1100",
    "JIZ": "1101",
    "OUT": "1110",
    "HLT": "1111"
}

# convert file into a string
def readFile(filename):
    with open(filename, 'r') as f:
        assembly = f.read()
    return assembly

# write binary back into a file
def writeFile(filename, machineCode):
    with open(filename, 'w') as f:
        f.write(str(machineCode))

# First pass: Collect labels
def pass1(assembly_code):
    labels = {}
    address = 0
    lines = assembly_code.split('\n')
    for line in lines:
        # Match labels
        label_match = re.match(r"(\w+):", line)
        if label_match:
            labels[label_match.group(1)] = address
        # Count instruction bytes
        if re.match(r"\s*\w+", line):
            address += 1
    return labels

# Second pass: Replace labels and translate to binary
def pass2(assembly_code, labels):
    binary_code = []
    lines = assembly_code.split('\n')
    for line in lines:
        # Remove comments and strip whitespace
        line = re.sub(r";.*", "", line).strip()
        if not line:
            continue
        # Translate instructions
        parts = line.split()
        if parts[0] in opcodes:
            opcode = opcodes[parts[0]]
            if len(parts) > 1:
                # Replace labels with addresses
                operand = parts[1]
                if operand in labels:
                    operand = format(labels[operand], '08b')  # 8-bit address
                else:
                    operand = format(int(operand), '08b')  # Immediate value
                # Generate output with comma-separated bytes
                binary_code.append(f"{opcode},{operand}")
            else:
                binary_code.append(f"{opcode},00000000")  # No operand
    return binary_code

# Example usage
assembly_code = """
start:
LDA 50
ADD 10
STA 51
JMP start
HLT
"""

assembly = readFile('test.asm')
labels = pass1(assembly)
binary_code = pass2(assembly, labels)
writeFile('test.txt', binary_code)

# Print the output with comma-separated bytes
for line in binary_code:
    print(line)

if __name__ == '__main__':
    pass