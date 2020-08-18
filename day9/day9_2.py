#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode
from intcode_parser import IntComputer
# Input Parse
puzzle = AdventOfCode(year=2019, day=9)
puzzle_input = puzzle.get_input()

# Actual Code
computer = IntComputer(
    code=[int(i) for i in puzzle_input.split(",")],
    inputs=lambda _: 2
)
for _ in computer:
    if computer.outputs:
        print(computer.outputs.pop())
# print(computer.outputs)

# Result
# print(computer.outputs)