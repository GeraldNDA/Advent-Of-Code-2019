#!/usr/bin/env python3
# Imports
from intcode_parser import IntComputer
from enum import Enum
from collections import defaultdict
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=15)
puzzle_input = puzzle.get_input()

class Point(object):

    __slots__ = ["x", "y"]

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __neg__(self) -> 'Point':
        return Point(-self.x, -self.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return self + (-other)

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other: 'Point') -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

class Directions(Enum):
    NORTH = Point(0, -1)
    SOUTH = Point(0, +1)
    WEST = Point(-1, 0)
    EAST = Point(+1, 0)

    def opposite(self):
        point: Point = self.value
        return Directions(-point)

    def movement_command(self):
        if self is Directions.NORTH:
            return 1
        elif self is Directions.SOUTH:
            return 2
        elif self is Directions.WEST:
            return 3
        elif self is Directions.EAST:
            return 4


class DroidController(object):
    def __init__(self, remote_controller):
        self.droid = IntComputer(code=remote_controller, inputs=self.move)
        self.curr_pos = Point(x=0, y=0)
        self.curr_path = []
        self.tried = defaultdict(set)
        self.command_generator = self.get_next()
        self.backtracking = False
        self.last_dir = None
        self.done = False
    
    def backtrack(self):
        self.backtracking = True
        while not self.next_dirs():
            new_dir = self.curr_path.pop()
            new_dir = new_dir.opposite()
            yield new_dir
        self.backtracking = False

    def next_dirs(self):
        to_try = set(d for d in Directions) - self.tried[self.curr_pos]
        if self.curr_path:
            to_try.discard(self.curr_path[-1].opposite())
        return to_try

    def get_next(self):
        while not self.done:
            # Tries to backtrack if necessary
            for new_dir in self.backtrack():
                if len(self.curr_path) == 1:
                    raise ValueError
                yield new_dir
            to_try = self.next_dirs()
            new_dir = to_try.pop()
            yield new_dir
        # compute will handle updating current position and tried list
    
    def move(self, _):
        next_dir =  next(self.command_generator)
        self.last_dir = next_dir
        self.tried[self.curr_pos].add(next_dir)
        

        command =  next_dir.movement_command()
        return command
    
    def explore(self):
        for _ in self.droid:
            # print(">", _)
            if self.droid.outputs:
                if self.done:
                    raise ValueError("Expected program to halt or smtg ...")
                response = self.droid.outputs.pop()
                if response:
                    self.curr_pos += self.last_dir.value
                    if not self.backtracking:
                        self.curr_path.append(self.last_dir)
                    self.last_dir = None
                else:
                    assert not self.backtracking
                if response == 2:
                    self.done = True
                # print(response, self.curr_pos, self.curr_path, self.tried[self.curr_pos])
        else:
            if not self.done:
                raise ValueError("Expected more execution ...")



        
    
# Actual Code
controller = DroidController([int(instr) for instr in puzzle_input.split(",")])
controller.explore()


# Result
print(len(controller.curr_path))