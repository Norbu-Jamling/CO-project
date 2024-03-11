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