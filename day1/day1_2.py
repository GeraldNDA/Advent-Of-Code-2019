#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=1)
puzzle_input = puzzle.get_input()

# Actual Code
modules = map(int, puzzle_input)
def get_required_fuel(module):
    total = 0
    while module > 0:
        module = module // 3 - 2
        total += max(module, 0)
    return total

# Result
print(sum(map(get_required_fuel, modules)))