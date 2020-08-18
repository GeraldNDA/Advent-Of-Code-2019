#!/usr/bin/env python3
# Imports
from collections import defaultdict
from intcode_parser import IntComputer

from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=13)
puzzle_input = puzzle.get_input()

# Actual Code
arcade_machine = [int(i) for i in puzzle_input.split(",")]
computer = IntComputer(
    code=list(arcade_machine)
)

# Get map
game_map = {}
walls = set()
blocks = []
paddle_pos = None
last_ball_pos = None
ball_pos = None

def shift_joystick(idx):
    # draw_map()
    if last_ball_pos:
        ball_x_dir = ball_pos[0] - last_ball_pos[0]
        next_x =  ball_x_dir + ball_pos[0]
        if ball_x_dir*(next_x - paddle_pos[0]) > 1:
            return ball_x_dir
    return 0

def draw_map():
    for c in range(23):
        for r in range(42):
            assert (r, c) in game_map
            tile_id = game_map[(r, c)]
            if tile_id == 4:
                print("O", end="")
            elif tile_id == 3:
                print("̅ ", end="")
            # Should only happen once
            elif tile_id == 2:
                print("░", end="")
            elif tile_id == 1:
                print("▓", end="")
            else:
                print(" ", end="")
        print()
    print(f"ball_pos={last_ball_pos}->{ball_pos}, paddle_pos={paddle_pos}")

arcade_machine[0] = 2
score = 0
building_map = True
computer = IntComputer(
    code=arcade_machine,
    inputs=shift_joystick
)
for _ in computer:
    if len(computer.outputs) == 3:
        # print(computer.outputs)
        pos = (computer.outputs[0], computer.outputs[1])
        if pos == (-1, 0):
            score = computer.outputs[2]
            building_map = False
        else:
            tile_id = computer.outputs[2]
            if tile_id == 4:
                last_ball_pos, ball_pos = ball_pos, pos
                # draw_map()
            elif tile_id == 3: 
                if not building_map:
                    game_map[paddle_pos] = 0
                paddle_pos = pos
            # Should only happen once
            elif tile_id == 2:
                blocks.append(pos)
            elif tile_id == 1:
                walls.add(pos)
            game_map[pos] = tile_id
        computer.outputs = []
# Draw map:


# Result
print(score)