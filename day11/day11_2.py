#!/usr/bin/env python3
# Imports
from intcode_parser import IntComputer
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=11)
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

class Robot(object):
    DIRECTIONS = (
        Point(0,-1), # UP
        Point(1, 0), # RIGHT
        Point(0,1), #DOWN
        Point(-1,0), #LEFT
    )

    TEST_INSTR = [(0,1,0), (0,0,0), (0,1,0), (0,1,0), (1,0,1), (0,1,0), (0,1,0)]
    def __init__(self, brain_code) -> None:
        self.brain = IntComputer(
            code=brain_code,
            inputs=self.get_panel_color # All black
        )
        self.panels = {}
        self.curr_pos = Point(0,0)
        self.curr_dir = 0
    
    def get_panel_color(self, idx):
        if self.curr_pos not in self.panels:
            return 0 if idx != 0 else 1
        return self.panels[self.curr_pos]

    def paint_panel(self, color, turn_dir):
        assert color in (0, 1) and turn_dir in (0, 1)
        self.panels[self.curr_pos] = color
        if turn_dir:
            self.curr_dir += 1
        else:
            self.curr_dir -= 1
        self.curr_dir %= len(Robot.DIRECTIONS)
        self.curr_pos += Robot.DIRECTIONS[self.curr_dir]

    def paint(self):
        for _ in self.brain:
            if len(self.brain.outputs) == 2:
                # print(self.curr_pos, f"color={0 if self.curr_pos not in self.panels else self.panels[self.curr_pos]} dir={self.curr_dir}", end=" -> ")
                self.paint_panel(*self.brain.outputs)
                self.brain.outputs = []
                # print(self.curr_pos, f"color={color} dir={robo_dir}")
        
    def draw_panels(self):
        min_point = Point(x=0, y=0)
        max_point = Point(x=0, y=0)
        for point in self.panels:
            if point < min_point:
                min_point = point
            if point > min_point:
                max_point = point

        for y in range(min_point.y-3, max_point.y+3):
            for x in range(min_point.x-3, max_point.x+3):
                curr = Point(x=x, y=y)
                is_white = 0 if curr not in self.panels else self.panels[curr]
                print("▓" if is_white else "░", end="")
            print()

                    
    
    def test(self):
        for instr in Robot.TEST_INSTR:
            assert self.brain.get_input() is instr[0]
            print(self.curr_dir, self.curr_pos)
            self.paint_panel(*instr[1:])
        print(self.curr_dir, self.curr_pos)



painter = Robot(brain_code=[int(i) for i in puzzle_input.split(",")])
painter.paint()
# painter.test()


# Result
painter.draw_panels()