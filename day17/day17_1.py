#!/usr/bin/env python3
# Imports
from mapping import Directions, Point
from enum import Enum
from intcode_parser import IntComputer
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=17)
puzzle_input = puzzle.get_input()

camera_image = ""
computer = IntComputer(
    code=[int(i) for i in puzzle_input.split(",")]
)
for _ in computer:
    if computer.outputs:
        out = computer.outputs.pop()
        # print(out)
        camera_image += chr(out)

camera_image = camera_image.strip().splitlines()
width = len(camera_image[0])
height = len(camera_image)
total_alignment = 0
for y, row in enumerate(camera_image):
    for x, pixel in enumerate(row):
        pos = Point(x,y)
        if pixel != "#":
            continue
        possible_turns = 0
        for direction in Directions:
            new_pos = pos + direction.value
            if new_pos.in_image(width, height):
                try:
                    if camera_image[new_pos.y][new_pos.x] == "#":
                        possible_turns += 1
                except:
                    print(new_pos, len(ca), height)
                    raise
        if possible_turns == 4:
            alignment_param = x * y
            total_alignment += alignment_param
# Result
print(total_alignment)
# 851445