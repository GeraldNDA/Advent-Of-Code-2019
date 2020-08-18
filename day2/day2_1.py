#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=2)
puzzle_input = puzzle.get_input()

# Actual Code
program = [int(code) for code in puzzle_input.split(",")]
program[1] = 12
program[2] = 2

idx = 0
while program[idx] != 99:
    assert program[idx] in {1, 2}
    val1 = program[program[idx + 1]]
    val2 = program[program[idx + 2]]
    if program[idx] == 1:
        program[program[idx + 3]] = val1 + val2
    elif program[idx] == 2:
        program[program[idx + 3]] = val1 * val2
    idx += 4
# Result
print(program[0])