import re
from typing import Tuple

pattern_register = re.compile(r'Register [ABC]: (\d+)')
pattern_program = re.compile(r'Program: (.*)')

with open('input.txt') as f:
    A = int(pattern_register.match(f.readline()).group(1))
    B = int(pattern_register.match(f.readline()).group(1))
    C = int(pattern_register.match(f.readline()).group(1))
    f.readline()
    program = list(map(int, pattern_program.match(f.readline()).group(1).split(',')))

out = []

def execute(isp: int, A: int, B: int, C: int, opcode: int, operand: int) -> Tuple[int, int, int, int]:
    assert 0 <= opcode <= 7
    assert 0 <= operand <= 7

    new_isp = isp + 2

    if opcode in [0, 2, 5, 6, 7]:
        assert 0 <= operand <= 6
        if operand == 4:
            operand = A
        elif operand == 5:
            operand = B
        elif operand == 6:
            operand = C

    if opcode == 0:
        # avd instruction
        A = A >> operand
    elif opcode == 1:
        # bxl instruction
        B = B ^ operand
    elif opcode == 2:
        # bst instruction
        B = operand & 7
    elif opcode == 3:
        # jnz instruction
        if A != 0:
            new_isp = operand
    elif opcode == 4:
        # bxc instruction
        B = B ^ C
    elif opcode == 5:
        # out instruction
        out.append(operand & 7)
    elif opcode == 6:
        # bdv instruction
        B = A >> operand
    elif opcode == 7:
        # cdv instruction
        C = A >> operand

    isp = new_isp

    return isp, A, B, C

isp = 0
while isp < len(program):
    opcode = program[isp]
    operand = program[isp + 1]
    isp, A, B, C = execute(isp, A, B, C, opcode, operand)
    # print(f'{isp} {opcode} {operand}: {A} {B} {C} {out}')

with open('part1.txt', 'w') as f:
    f.write(','.join(map(str, out)))

# Part 2: Find the value of A to make the output same as the program
# Smart brute force, building A from prefix to get a desired suffix for the output

with open('input.txt') as f:
    A = int(pattern_register.match(f.readline()).group(1))
    B = int(pattern_register.match(f.readline()).group(1))
    C = int(pattern_register.match(f.readline()).group(1))
    f.readline()
    program = list(map(int, pattern_program.match(f.readline()).group(1).split(',')))

out = []

# for i in range(1 << 17):
#     A = i
#     B = 0
#     C = 0
#     out = []
#     isp = 0
#     while isp < len(program):
#         opcode = program[isp]
#         operand = program[isp + 1]
#         isp, A, B, C = execute(isp, A, B, C, opcode, operand)
#     if out == [4,0,5,5,3,0] and A == 0:
#         print(f'{i:017b}: {out} {A} {B} {C}')

# prefixs = ["11000000100001011", "11000000100001110", "11000000100011011", "11000100100001011", "11000100100001110", "11000110100001011", "11000110100001110", "11001000100001011", "11001000100001110", "11001000100011011"]
# arr = []
# for prefix in prefixs:
#     # Try extending the prefix to more digits
#     for num in range(15):
#         # Try extend num digits
#         for i in range(1 << num):
#             A = int(prefix + f'{i:0{num}b}', 2)
#             oldA = A
#             B = 0
#             C = 0
#             out = []
#             isp = 0
#             while isp < len(program):
#                 opcode = program[isp]
#                 operand = program[isp + 1]
#                 isp, A, B, C = execute(isp, A, B, C, opcode, operand)
#             if out == [0,3,4,0,5,5,3,0] and A == 0:
#                 print(f'{bin(oldA)[2:]}: {out} {A} {B} {C}')
#                 arr.append(bin(oldA)[2:])
# print(arr)

# prefixs = ['11000000100001011101110', '11000000100001110101001', '11000000100001110101110', '11000000100011011101110', '11000100100001011101110', '11000100100001110101001', '11000100100001110101110', '11000110100001011101110', '11000110100001110101001', '11000110100001110101110', '11001000100001011101110', '11001000100001110101001', '11001000100001110101110', '11001000100011011101110']
# arr = []
# for prefix in prefixs:
#     for num in range(15,16):
#         # Try extend num digits
#         for i in range(1 << num):
#             A = int(prefix + f'{i:0{num}b}', 2)
#             oldA = A
#             B = 0
#             C = 0
#             out = []
#             isp = 0
#             while isp < len(program):
#                 opcode = program[isp]
#                 operand = program[isp + 1]
#                 isp, A, B, C = execute(isp, A, B, C, opcode, operand)
#             if out == [5,7,5,1,6,0,3,4,0,5,5,3,0] and A == 0:
#                 print(f'{bin(oldA)[2:]}: {out} {A} {B} {C}')
#                 arr.append(bin(oldA)[2:])
# print(arr)

prefixs = ['11000000100001110101001001000010110100', '11000000100001110101001001011010110100', '11000000100001110101001001100010010100', '11000000100001110101001001100010110100', '11000000100001110101001001100100010100', '11000000100001110101001001100111010000', '11000000100001110101001001100111010100', '11000100100001110101001001000010110100', '11000100100001110101001001011010110100', '11000100100001110101001001100010010100', '11000100100001110101001001100010110100', '11000100100001110101001001100100010100', '11000100100001110101001001100111010000', '11000100100001110101001001100111010100', '11000110100001110101001001000010110100', '11000110100001110101001001011010110100', '11000110100001110101001001100010010100', '11000110100001110101001001100010110100', '11000110100001110101001001100100010100', '11000110100001110101001001100111010000', '11000110100001110101001001100111010100', '11001000100001110101001001000010110100', '11001000100001110101001001011010110100', '11001000100001110101001001100010010100', '11001000100001110101001001100010110100', '11001000100001110101001001100100010100', '11001000100001110101001001100111010000', '11001000100001110101001001100111010100']
for prefix in prefixs:
    for num in range(15):
        # Try extend num digits
        for i in range(1 << num):
            A = int(prefix + f'{i:0{num}b}', 2)
            oldA = A
            B = 0
            C = 0
            out = []
            isp = 0
            while isp < len(program):
                opcode = program[isp]
                operand = program[isp + 1]
                isp, A, B, C = execute(isp, A, B, C, opcode, operand)
            if out == [2,4,1,5,7,5,1,6,0,3,4,0,5,5,3,0] and A == 0:
                print(f'{bin(oldA)[2:]}: {out} {A} {B} {C} {oldA}')
                with open('part2.txt', 'w') as f:
                    f.write(str(oldA))
                exit()