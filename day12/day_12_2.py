#!/usr/bin/env python3
# Imports
import re
from math import gcd
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

    pos: Tuple[int]
    velocity: List[int]

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

    def __eq__(self, other):
        if not isinstance(other, Moon):
            return NotImplemented
        return self.pos == other.pos and self.velocity == other.velocity

class MoonTracker():

    moons: List[Moon]

    def __init__(self, moons: List[Moon]):
        self.steps = 0
        self.moons = moons
        self.initial_moons = [Moon(moon.pos) for moon in moons]
        self.patterns = [0,0,0]

    def __iter__(self):
        while True:
            for moon, other_moon in combinations(self.moons, 2):
                moon.apply_grav(other_moon)
                other_moon.apply_grav(moon)
            for moon in self.moons:
                moon.move()
            self.steps += 1
            for i in range(3):
                if self.patterns[i] != 0:
                    continue
                if all(moon.velocity[i] == 0 for moon in self.moons):
                    assert all(moon.pos[i] == initial_moon.pos[i] and moon.velocity[i] == initial_moon.velocity[i] for moon, initial_moon  in zip(self.moons, self.initial_moons))
                    print(i, self.steps)
                    self.patterns[i] = self.steps
            if any(pattern == 0 for pattern in self.patterns):
                yield self.steps
                continue
            break

# Actual Code
moon_tracker = MoonTracker([Moon.parse(line) for line in puzzle_input])

for _ in moon_tracker:
    pass
print(moon_tracker.patterns)
prod = 1
denom = 1
for pattern in moon_tracker.patterns:
    denom = gcd(denom, pattern)
    prod *= pattern
print(prod//denom)