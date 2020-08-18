#!/usr/bin/env python3
# Imports
from intcode_parser import IntComputer
from mapping import Point
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=19)
puzzle_input = puzzle.get_input()

# Actual Code
sim_code = [int(i) for i in puzzle_input.split(",")]


affected_points = 0
MAX_X, MAX_Y = 50, 50
for x in range(MAX_X):
    prev = affected_points
    for y in range(MAX_Y):
        def pos_gen():
            yield x
            yield y
        pos = pos_gen()
        drone_sim = IntComputer(
            code=list(sim_code),
            inputs=lambda _: next(pos)
        )
        for _ in drone_sim:
            pass
        assert len(drone_sim.outputs) == 1
        res = drone_sim.outputs.pop()
        print("#" if res else ".", end="")
        affected_points += res
    print(affected_points - prev)
print()


# Result
print(affected_points)