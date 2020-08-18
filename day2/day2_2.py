#!/usr/bin/env python3
# TODO: SHould probably use intcode_parser.py
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=2)
puzzle_input = puzzle.get_input()

# Actual Code
program = [int(code) for code in puzzle_input.split(",")]
program[1] = 12
program[2] = 2
def program_runner(program):
    program = list(program)
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
    return program

# Because brute force is sufficient ...
for noun in range(100):
    for verb in range(100):
        program[1] = noun
        program[2] = verb
        if program_runner(program)[0] == 19690720:
            print(noun*100 + verb)
            break
# Result
# print(noun*100 + verb)