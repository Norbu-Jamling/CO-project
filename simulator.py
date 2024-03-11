def parse_operands(instruction):
    opcode = instruction[:3]

    if opcode == '000':  # Add
        rd = int(instruction[3:8], 2)
        rs1 = int(instruction[8:13], 2)
        rs2 = int(instruction[13:], 2)
        return rd, rs1, rs2
    elif opcode == '010':  # Load Word
        rt = int(instruction[3:8], 2)
        offset = int(instruction[8:15], 2)
        rs = int(instruction[15:], 2)
        return rt, offset, rs
    elif opcode == '111':  # New Instruction
        rt = int(instruction[3:8], 2)
        imm = int(instruction[8:], 2)
        return rt, imm
    elif opcode == '001':  # Subtract
        rd = int(instruction[3:8], 2)
        rs1 = int(instruction[8:13], 2)
        rs2 = int(instruction[13:], 2)
        return rd, rs1, rs2

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


