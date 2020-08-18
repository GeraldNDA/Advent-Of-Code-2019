#!/usr/bin/env python3
# Imports
import re
from typing import List, Tuple, Dict, Text
from typing import Sequence, Union, Optional, Iterable
from itertools import combinations

from aoc import AdventOfCode


# Input Parse
puzzle = AdventOfCode(year=2019, day=12)
puzzle_input = puzzle.get_input()
# puzzle_input = [
#     "<x=-1, y=0, z=2>",
#     "<x=2, y=-10, z=-7>",
#     "<x=4, y=-8, z=8>",
#     "<x=3, y=5, z=-1>",
# ]

class Moon(object):
    MOON_LINE_MATCHER = re.compile(r"<x=(-?\d+), y=(-?\d+), z=(-?\d+)>")
    
    def __init__(self, pos: Tuple[int]) -> None:
        self.pos = pos
        self.velocity = [0,0,0]

    @staticmethod
    def parse(line: str) -> 'Moon':
        moon_info = Moon.MOON_LINE_MATCHER.match(line)
        if not moon_info:
            raise ValueError(line)
        else:
            moon_info = moon_info.groups()
            return Moon(list(map(int, moon_info[0:3])))
    
    def apply_grav(self, moon: 'Moon') -> None:
        for idx, (self_pos, other_pos) in enumerate(zip(self.pos, moon.pos)):
            if self_pos < other_pos:
                self.velocity[idx] += 1
            elif self_pos > other_pos:
                self.velocity[idx] -= 1

    def move(self) -> None:
        for idx, self_vel in enumerate(self.velocity):
            self.pos[idx] += self_vel
    
    def energy(self) -> int:
        return sum(map(abs, self.pos)) * sum(map(abs, self.velocity))

    def __repr__(self) -> str:
        return f"Moon(pos={tuple(self.pos)}, vel={tuple(self.velocity)})"




    
# Actual Code
moons = [Moon.parse(line) for line in puzzle_input]

for _ in range(1000):
    for moon, other_moon in combinations(moons, 2):
            moon.apply_grav(other_moon)
            other_moon.apply_grav(moon)
    for moon in moons:
        moon.move()

# Result
print(sum(moon.energy() for moon in moons))