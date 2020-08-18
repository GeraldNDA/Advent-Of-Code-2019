#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=3)
puzzle_input = puzzle.get_input()

# Actual Code
wire1, wire2 = [wire.split(",") for wire in puzzle_input]
start = (0,0)
used_points = {start: 0}
dirs = {
    "U": (0, 1),
    "D": (0, -1),
    "L": (-1, 0),
    "R": (1, 0),
}
curr = start
steps = 0
print("BUILDING SEGMENT 1")
for segment in wire1:
    dir = segment[0]
    amount = int(segment[1:])
    for i in range(amount):
        steps += 1
        curr = tuple(sum(p) for p in zip(dirs[dir], curr))
        used_points[curr] = steps

best_point = None
best_steps = 0
curr = start
steps = 0
print("BUILDING SEGMENT 2")
for segment in wire2:
    dir = segment[0]
    amount = int(segment[1:])
    for i in range(amount):
        steps += 1
        curr = tuple(sum(p) for p in zip(dirs[dir], curr))
        if curr in used_points:
            if best_point is None or steps + used_points[curr] < best_steps:
                best_point = curr
                best_steps = steps + used_points[curr]


# Result
print(best_point, best_steps)