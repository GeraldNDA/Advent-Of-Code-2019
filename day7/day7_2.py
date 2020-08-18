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
for amp_phases in permutations(range(5, 10)):
    amps = []
    amp_input = 0
    for amp_idx in range(5):
        amp = IntComputer(list(code), inputs=(lambda phase: lambda idx: phase if idx == 0 else amp_input)(amp_phases[amp_idx]))
        amps.append((amp_idx, amp))
    done = False
    while not done:
        amp_idx, amp = amps.pop(0)
        for _ in amp:
            if len(amp.outputs):
                assert len(amp.outputs) == 1
                amp_input = amp.outputs.pop()
                break
        else:
            if amp_idx == 4:
                done = True
                max_output = max(amp_input, max_output)
                if max_output == amp_input:
                    print(amp_phases, max_output)
        amps.append((amp_idx, amp))
        
        # print(amp_input)

# Result
print(max_output)