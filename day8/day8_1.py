#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=8)
puzzle_input = puzzle.get_input()
WIDTH, HEIGHT = 25, 6


# Actual Code
layers = [puzzle_input[i:i + WIDTH*HEIGHT] for i in range(0, len(puzzle_input), WIDTH * HEIGHT)]
print(layers)
min_layer = min(layers, key=lambda l: l.count("0"))
check = min_layer.count("1") * min_layer.count("2")


# Result
print(check)