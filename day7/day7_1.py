#!/usr/bin/env python3
# Imports
from itertools import permutations
from intcode_parser import IntComputer
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=7)
puzzle_input = puzzle.get_input()
# puzzle_input = "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"

# Actual Code
code = [int(line) for line in puzzle_input.split(",")]

max_output = 0
for amp_phases in permutations(range(5)):
    amp_input = 0
    for amp_idx in range(5):
        amp = IntComputer(list(code), inputs=(lambda phase: lambda idx: phase if idx == 0 else amp_input )(amp_phases[amp_idx]))
        for _ in amp:
            pass
        assert len(amp.outputs) == 1
        amp_input = amp.outputs[0]
        # print(amp_input)
    max_output = max(amp_input, max_output)
    if max_output == amp_input:
        print(amp_phases, max_output)

# Result
print(max_output)