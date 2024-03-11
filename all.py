assembler implementation




def validate_instruction(mnemonic, operands):
    if mnemonic not in ['add', 'sub', 'lw', 'sw', 'new_instr']:
        raise ValueError(f"Invalid mnemonic: {mnemonic}")

    if mnemonic in ['add', 'sub']:
        if len(operands) != 3:
            raise ValueError(f"Invalid number of operands for {mnemonic}: {len(operands)}")
    elif mnemonic in ['lw', 'sw']:
        if len(operands) != 3:
            raise ValueError(f"Invalid number of operands for {mnemonic}: {len(operands)}")
    elif mnemonic == 'new_instr':
        if len(operands) != 2:
            raise ValueError(f"Invalid number of operands for {mnemonic}: {len(operands)}")
        if not operands[1].isdigit():
            raise ValueError("Immediate value must be a number")

def parse_operands(mnemonic, operands):
    if mnemonic in ['add', 'sub']:
        rd, rs1, rs2 = operands
        return rd, rs1, rs2
    elif mnemonic in ['lw', 'sw']:
        rt, offset, rs = operands
        return rt, offset, rs
    elif mnemonic == 'new_instr':
        rt, imm = operands
        return rt, imm

def assemble_instruction(mnemonic, operands):
    opcodes = {
        'add': '000',
        'sub': '001',
        'lw': '010',
        'sw': '011',
        'new_instr': '111',
    }

    validate_instruction(mnemonic, operands)

    opcode = opcodes[mnemonic]

    if mnemonic in ['add', 'sub']:
        rd, rs1, rs2 = parse_operands(mnemonic, operands)
        binary_operands = [format(int(rd[1:]), '05b'), format(int(rs1[1:]), '05b'), format(int(rs2[1:]), '05b')]
    elif mnemonic in ['lw', 'sw']:
        rt, offset, rs = parse_operands(mnemonic, operands)
        binary_operands = [format(int(rt[1:]), '05b'), format(int(rs[1:]), '05b'), format(int(offset), '07b')]
    elif mnemonic == 'new_instr':
        rt, imm = parse_operands(mnemonic, operands)
        binary_operands = [format(int(rt[1:]), '05b'), format(int(imm), '07b')]

    binary_instruction = opcode + ''.join(binary_operands)

    return binary_instruction


simulator implementation



def execute_instruction(instruction, registers, memory, pc):
    opcode = instruction[:3]

    if opcode == '000':  # Add
        rd, rs1, rs2 = parse_operands(instruction)
        registers[rd] = registers[rs1] + registers[rs2]
        pc += 1
    elif opcode == '001':  # Sub
        rd, rs1, rs2 = parse_operands(instruction)
        registers[rd] = registers[rs1] - registers[rs2]
        pc += 1
    elif opcode == '010':  # Load Word
        rt, offset, rs = parse_operands(instruction)
        addr = registers[rs] + int(offset)
        registers[rt] = memory[addr]
        pc += 1
    elif opcode == '011':  # Store Word
        rt, offset, rs = parse_operands(instruction)
        addr = registers[rs] + int(offset)
        memory[addr] = registers[rt]
        pc += 1
    elif opcode == '111':  # New Instruction
        rt, imm = parse_operands(instruction)
        registers[rt] = int(imm)
        pc += 1
    else:
        raise ValueError("Invalid opcode")

    return pc

assembly code for 
simple and hard test case



# Simple Test Case
add r1, r2, r3    # Add r2 and r3, store result in r1
sub r4, r5, r6    # Subtract r6 from r5, store result in r4
lw r7, 10(r8)     # Load value from memory address 10 + value in r8, store in r7
sw r9, 20(r10)    # Store value in r9 to memory address 20 + value in r10

# Hard Test Case
loop_start:
    add r11, r12, r13   # Add r12 and r13, store result in r11
    sub r14, r15, r16   # Subtract r16 from r15, store result in r14
    lw r17, 30(r18)     # Load value from memory address 30 + value in r18, store in r17
    sw r19, 40(r20)     # Store value in r19 to memory address 40 + value in r20
    new_instr r21, 50   # Perform new instruction with immediate value 50
    # Branching example
    beq r22, r23, loop_end   # Branch to loop_end if r22 equals r23
    addi r18, r18, 1   # Increment r18
    j loop_start        # Jump back to loop_start
loop_end:

to generate a binary file 



def assemble_test_program(input_file, output_file):
    with open(input_file, 'r') as f:
        assembly_code = f.readlines()

    binary_instructions = []
    for line in assembly_code:
        mnemonic, operands = parse_instruction(line)
        binary_instruction = assemble_instruction(mnemonic, operands)
        binary_instructions.append(binary_instruction)

    write_binary(binary_instructions, output_file)

# Example usage
assemble_test_program('test_program.s', 'test_program.bin')

in simulator 
to trace simple and hard test cases


def execute_test_program(memory):
    registers = [0] * 32  # Initialize registers
    pc = 0  # Program counter
    trace = []

    while pc < len(memory):
        instruction = format(memory[pc], '08b')  # Fetch instruction from memory
        trace.append({'pc': pc, 'instruction': instruction, 'registers': list(registers), 'memory': list(memory)})
        pc = execute_instruction(instruction, registers, memory, pc)  # Execute instruction

    return trace

# Example usage
memory = load_program('test_program.bin')
trace = execute_test_program(memory)

# Test Case Generating Errors

# Attempt to use an undefined instruction
invalid_instr r1, r2, r3

# Attempt to use an invalid register index
add r1, r2, r33

# Attempt to access memory beyond the allowed range
lw r4, 100(r0)

# Attempt to store a value to a non-existent memory address
sw r5, 0x10000000(r0)

# Attempt to perform a division by zero
div r6, r7, r0