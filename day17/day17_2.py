#!/usr/bin/env python3
# Imports
from mapping import Directions, Turn, Point
from enum import Enum
from intcode_parser import IntComputer
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=17)
puzzle_input = puzzle.get_input()

class Instruction(object):
    def __init__(self, todo):
        self.task = todo
    
    def __eq__(self, other):
        if isinstance(other, Instruction):
            return self.task == other.task
        return False
    
    def __repr__(self):
        return f"Instruction({self.task})"

    def __str__(self):
        return f"{self.task if not isinstance(self.task, Turn) else self.task.value}"

    

# Get scaffold image
robot_code = [int(i) for i in puzzle_input.split(",")]
camera_image = ""
computer = IntComputer(
    code=list(robot_code)
)
for _ in computer:
    if computer.outputs:
        out = computer.outputs.pop()
        # print(out)
        camera_image += chr(out)

print(camera_image)
# Parse locations on scaffold image
camera_image = camera_image.strip().splitlines()
width = len(camera_image[0])
height = len(camera_image)


start_dir = Directions.NORTH
start_pos = None
scaffold = set()
for row_idx, row in enumerate(camera_image):
    for col_idx, pixel in enumerate(row):
        if pixel in "#^":
            curr_point = Point(col_idx, row_idx)
            if pixel == "^":
                assert start_pos is None
                start_pos = curr_point
            scaffold.add(curr_point)

print(start_pos, start_dir)
path = []
done = False
while not done:
    for turn_type in Turn:
        new_dir = start_dir + turn_type
        new_pos = start_pos + new_dir
        if new_pos in scaffold:
            steps = 0
            while (new_pos + new_dir * steps) in scaffold:
                steps += 1
            path.extend([Instruction(turn_type), Instruction(steps)])
            start_pos = new_pos + new_dir * (steps - 1)
            start_dir = new_dir
            print([Instruction(turn_type), Instruction(steps)])
            break
    else:
        break
# print(start_pos)

func_sets = {
    "A": [Instruction(Turn.LEFT), Instruction(10), Instruction(Turn.RIGHT), Instruction(12), Instruction(Turn.RIGHT), Instruction(12)],
    "B": [Instruction(Turn.RIGHT), Instruction(6), Instruction(Turn.RIGHT), Instruction(10), Instruction(Turn.LEFT), Instruction(10)],
    "C": [Instruction(Turn.RIGHT), Instruction(10), Instruction(Turn.LEFT), Instruction(10), Instruction(Turn.LEFT), Instruction(12), Instruction(Turn.RIGHT), Instruction(6)]
}
def instr_subsets(instr_set, instructions):
    matches = set()
    for start_idx in range(len(instructions) - len(instr_set) + 1):
        if instructions[start_idx:start_idx+len(instr_set)] == instr_set:
            matches.add(start_idx)
    return matches

max_lens = {func: len(path) for func in "ABC"}
# Technically, this algorithm could be improved by looking ahead and seeing if the limit should be applied to "A" or "B".
# Because of the input, limitting "A" is sufficient to utilize the greedy algorithm
while not done:
    temp_path = list(path)
    start_idx = 0
    for func in "ABC":
        while not isinstance(temp_path[start_idx], Instruction):
            start_idx += 1
        max_end_idx = min(max_lens[func]+start_idx, len(temp_path))
        # print(func, max_end_idx)
        for end_idx in range(max_end_idx, start_idx, -1):
            if any(isinstance(instr, str) for instr in temp_path[start_idx:end_idx]):
                continue
            duplicate_sets = instr_subsets(temp_path[start_idx:end_idx], temp_path[end_idx:])
            if duplicate_sets:
                func_sets[func] = temp_path[start_idx:end_idx]
                func_size = len(temp_path[start_idx:end_idx])
                # print(func, func_size, "=>",  temp_path[start_idx:end_idx], "*", len(duplicate_sets) + 1)
                for duplicate_idx in {dupe + end_idx for dupe in duplicate_sets} | {start_idx,}:
                    temp_path[duplicate_idx:duplicate_idx+func_size] = [func]*func_size
                break
    if all(isinstance(instr, str) for instr in temp_path):
        break
    else:
        max_lens["A"] = len(func_sets["A"]) - 1
        if max_lens["A"] == 0:
            raise ValueError
        # print(max_lens)

for func, func_set in func_sets.items():
    duplicate_sets = instr_subsets(func_set, path)
    assert duplicate_sets
    func_size = len(func_set)
    # print(func, func_size, "=>", func_set, "*", len(duplicate_sets) + 1)
    for duplicate_idx in duplicate_sets:
        path[duplicate_idx:duplicate_idx+func_size] = [func]*func_size
# print(path)

short_path = []
idx = 0
while idx < len(path):
    assert path[idx] in func_sets
    short_path.append(path[idx])
    idx += len(func_sets[path[idx]])
assert idx == len(path)

# Gives almost correct result .... but greedy algorithm is bad

print(short_path)

def input_instr(debug=False):
    for step in ",".join(short_path):
        yield ord(step)
    yield ord("\n")

    for func in "ABC":
        for step in ",".join(map(str, func_sets[func])):
            yield ord(step)
        yield ord("\n")
    
    yield ord("y" if debug else "n")
    yield ord("\n")


robot_code[0] = 2
input_gen = input_instr()
vacuum_robo = IntComputer(
    code=list(robot_code),
    inputs=lambda _: next(input_gen)
)
for _ in vacuum_robo:
    if vacuum_robo.outputs:
        out = vacuum_robo.outputs.pop()
        if out < (1 << 8):
            print(chr(out), end="")
        else:
            print(out)