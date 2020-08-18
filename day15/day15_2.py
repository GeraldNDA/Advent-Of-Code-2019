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
    
    def __lt__(self, other: 'Point') -> bool:
        return (self.x + self.y) < (other.x + other.y)
   
    def __gt__(self, other: 'Point') -> bool:
        return (self.x + self.y) > (other.x + other.y)

class Directions(Enum):
    NORTH = Point(0, -1)
    SOUTH = Point(0, +1)
    WEST = Point(-1, 0)
    EAST = Point(+1, 0)

    def opposite(self):
        point = self.value
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
    def __init__(self, remote_controller, avoid=None):
        self.droid = IntComputer(code=remote_controller, inputs=self.move)
        self.curr_pos = Point(x=0, y=0)
        self.curr_path = []
        self.tried = defaultdict(set)
        self.command_generator = self.get_next()
        self.backtracking = False
        self.last_dir = None
        self.done = False
        self.avoid = DroidController.path_to_pos(avoid) if avoid else set()
        self.map = {self.curr_pos: 0}
    
    @staticmethod
    def path_to_pos(path):
        poses = []
        curr_pos = Point(x=0, y=0)
        for curr_dir in path:
            poses.append(curr_pos)
            curr_pos += curr_dir.value
        poses.append(curr_pos)
        return poses
    
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
            # Avoid dirs to avoid
            new_dir =  sorted(to_try, key=lambda d: (self.curr_pos + d.value) in self.avoid)[0]
            yield new_dir
        # compute will handle updating current position and tried list
    
    def move(self, _):
        next_dir =  next(self.command_generator)
        self.last_dir = next_dir
        self.tried[self.curr_pos].add(next_dir)
        

        command =  next_dir.movement_command()
        return command
    
    def explore(self, should_map=False):
        for _ in self.droid:
            # print(">", _)
            if self.droid.outputs:
                if self.done:
                    raise ValueError("Expected program to halt or smtg ...")
                response = self.droid.outputs.pop()
                checked = self.curr_pos + self.last_dir.value
                if should_map:
                    self.map[checked] = response
                if response:
                    self.curr_pos = checked
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

    def fill_map(self):
        assert self.map[self.curr_pos] == 2
        minutes = 0
        seen = set()
        wavefront = [self.curr_pos]
        while wavefront:
            for _ in range(len(wavefront)):
                point = wavefront.pop(0)
                seen.add(point)
                for direction in Directions:
                    new_point = point + direction.value
                    if new_point not in seen and self.map[new_point]:
                        wavefront.append(new_point)
            minutes += 1
        return minutes - 1
    
    def draw_map(self):
        min_point = Point(x=0, y=0)
        max_point = Point(x=0, y=0)
        for point in self.map:
            if point < min_point:
                min_point = point
            if point > min_point:
                max_point = point

        for y in range(min_point.y-1, max_point.y+8):
            for x in range(min_point.x-1, max_point.x+36):
                curr = Point(x=x, y=y)
                if curr not in self.map or not self.map[curr]:
                    render = "▓"
                elif self.map[curr] == 1:
                    render = "░"
                elif self.map[curr] == 2:
                    render = "X"
                if curr == Point(0,0):
                    render = "0"
                print(render, end="")
            print()


        
    
# Actual Code
controller = DroidController([int(instr) for instr in puzzle_input.split(",")])
controller.explore()
correct_path = controller.curr_path
mapping_robot = DroidController([int(instr) for instr in puzzle_input.split(",")], avoid=correct_path)
mapping_robot.explore(should_map=True)
mapping_robot.draw_map()





# Result
print(mapping_robot.fill_map())
# print(len(controller.curr_path))