#!/usr/bin/env python3
# Imports
from intcode_parser import IntComputer

from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=13)
puzzle_input = puzzle.get_input()

# Actual Code
computer = IntComputer(
    code=[int(i) for i in puzzle_input.split(",")],
    inputs=lambda _: 1
)

objects = {}
block_count = 0
for _ in computer:
    if len(computer.outputs) == 3:
        objects[(computer.outputs[0], computer.outputs[1])] = computer.outputs[2]
        if computer.outputs[2] == 2:
            block_count += 1
        computer.outputs = []

# Result
print(block_count)