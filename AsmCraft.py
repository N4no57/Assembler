import re
import sys
import os

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

# write binary back into a file
def writeFile(filename, machineCode):
    outputCode = ""
    for line in machineCode:
        outputCode += line + '\n'
    with open(filename, 'w') as f:
        f.write(str(outputCode))

# First pass: Collect labels
def pass1(assembly_code):
    labels = {}
    address = 0
    lines = assembly_code.split('\n')
    for line in lines:
        # Match labels
        label_match = re.match(r"(\w+):", line)
        if label_match:
            label_name = label_match.group(1)
            if label_name in labels:
                print(f"Error: duplicate label {label_name} at address {address}")
                return None
            labels[label_match.group(1)] = address
        # Count instruction bytes
        if re.match(r"\s*\w+", line):
            address += 1
    return labels

# Second pass: Replace labels with addresses and translate to binary
def pass2(assembly_code, labels):
    binary_code = []
    lines = assembly_code.split('\n')
    for line in lines:
        # Remove comments and strip whitespace
        line = re.sub(r";.*", "", line).strip()
        if not line:
            continue

        # Skip label definitions in the second pass
        if re.match(r"\w+:", line):
            continue

        # Translate instructions
        parts = line.split()
        if not parts:
            continue
        instruction = parts[0]
        if instruction in opcodes:
            opcode = opcodes[instruction]
            if len(parts) > 1:
                operand = parts[1]
                if operand in labels:
                    operand = format(labels[operand], '08b')  # 8-bit address
                else:
                    try:
                        # Convert operand to an 8-bit binary string
                        operand_value = int(operand)
                        if operand_value < 0 or operand_value > 255:
                            print(f"Error: Operand '{operand}' out of range (0-255)")
                            return None  # Indicate an error occurred
                        operand = format(operand_value, '08b')
                    except ValueError:
                        print(f"Error: Invalid operand '{operand}'")
                        return None  # Indicate an error occurred
                binary_code.append(f"{opcode}, {operand}")
            else:
                binary_code.append(f"{opcode}, 00000000")  # No operand
        else:
            print(f"Error: Unknown instruction '{instruction}'")
            return None  # Indicate an error occurred
    return binary_code


def assemble_file(filename, name):
    try:
        with open(filename, 'r') as f:
            assembly = f.read()
    except FileNotFoundError:
        print(f"Error: File {filename} not found")
        return

    labels = pass1(assembly)
    if labels is None:
        return

    binary_code = pass2(assembly, labels)
    if binary_code is None:
        return
    
    writeFile(name + ".txt", binary_code)

    

if __name__ == '__main__':
    filename = sys.argv[1]
    name, extension = os.path.splitext(filename)
    assemble_file(filename, name)
    