#!/usr/bin/env python3
# Imports
from intcode_parser import IntComputer
from mapping import Point, Directions
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=19)
puzzle_input = puzzle.get_input()
sim_code = [int(i) for i in puzzle_input.split(",")]

# Actual Code
def check_point(row, col):
    def pos_gen():
        yield col # column is the x position
        yield row # row is the y position 
    pos = pos_gen()
    drone_sim = IntComputer(
        code=list(sim_code),
        inputs=lambda _: next(pos)
    )
    for _ in drone_sim:
        pass
    assert len(drone_sim.outputs) == 1
    res =  drone_sim.outputs.pop()
    # print(f"{row} {col} => {res}")
    return res

# def check_point(row, col):
#     grid = [
#     "#.......................................",
#     ".#......................................",
#     "..##....................................",
#     "...###..................................",
#     "....###.................................",
#     ".....####...............................",
#     "......#####.............................",
#     "......######............................",
#     ".......#######..........................",
#     "........########........................",
#     ".........#########......................",
#     "..........#########.....................",
#     "...........##########...................",
#     "...........############.................",
#     "............############................",
#     ".............#############..............",
#     "..............##############............",
#     "...............###############..........",
#     "................###############.........",
#     "................#################.......",
#     ".................########OOOOOOOOOO.....",
#     "..................#######OOOOOOOOOO#....",
#     "...................######OOOOOOOOOO###..",
#     "....................#####OOOOOOOOOO#####",
#     ".....................####OOOOOOOOOO#####",
#     ".....................####OOOOOOOOOO#####",
#     "......................###OOOOOOOOOO#####",
#     ".......................##OOOOOOOOOO#####",
#     "........................#OOOOOOOOOO#####",
#     ".........................OOOOOOOOOO#####",
#     "..........................##############",
#     "..........................##############",
#     "...........................#############",
#     "............................############",
#     ".............................###########",
#     ]
#     if row >= len(grid):
#         raise ValueError("Too many rows")
#     if col >= len(grid[0]):
#         return 0
#     return int(grid[row][col] != ".")

SHIP_SIZE = 100
MAX_CHECK = 10

row_info = set()
last_row_start = 0
row_idx = 0

done = False
while not done:
    print(f"{row_idx} -> {last_row_start}", end="\r")
    for start in range(last_row_start, last_row_start + MAX_CHECK):
        if check_point(row_idx, start):
            break
    else:
        start = 0
    # Check if can fit ship on this row
    if check_point(row_idx, start + (SHIP_SIZE-1)):
        # store row information
        if check_point(row_idx - (SHIP_SIZE-1), start + (SHIP_SIZE-1)):
            # Row and column values are swapped
            best_point = start*1_00_00 + row_idx - (SHIP_SIZE - 1)
            print()
            print(f"Best point is {best_point}")
            break
    last_row_start = start - 1
    row_idx += 1