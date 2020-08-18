#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode
from intcode_parser import IntComputer

# Input Parse
puzzle = AdventOfCode(year=2019, day=5)
puzzle_input = puzzle.get_input()
program = [int(code) for code in puzzle_input.split(",")]

# Actual Code
ship_id=5
computer = IntComputer(code=program, inputs=lambda _: ship_id)
for curr_instr in computer:
    print(">", curr_instr)



# Result
print(computer.outputs)