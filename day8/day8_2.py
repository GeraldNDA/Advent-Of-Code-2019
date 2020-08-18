#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=8)
puzzle_input = puzzle.get_input()
WIDTH, HEIGHT = 25, 6


# Actual Code
image = [puzzle_input[i:i + WIDTH*HEIGHT] for i in range(0, len(puzzle_input), WIDTH * HEIGHT)]
final_im = []
for pix in range(WIDTH * HEIGHT):
    for layer in image:
        if layer[pix] == '2':
            continue
        final_im.append(layer[pix])
        break

# Result
for i in range(len(final_im)):
    print(" " if final_im[i] == "0" else "*", end="")
    if i % WIDTH == WIDTH - 1:
        print()