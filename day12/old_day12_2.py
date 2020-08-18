#!/usr/bin/env python3
# Imports
import re
from typing import List, Tuple, Dict, Text
from typing import Sequence, Union, Optional, Iterable
from collections import defaultdict
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
puzzle_input = [
    "<x=-8, y=-10, z=0>",
    "<x=5, y=5, z=10>",
    "<x=2, y=-7, z=3>",
    "<x=9, y=-8, z=-3>",
]

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
    
    def apply_grav(self, grav) -> None:
        for idx, grav_weight in enumerate(grav):
            self.velocity[idx] += grav_weight

    def move(self) -> None:
        for idx, self_vel in enumerate(self.velocity):
            self.pos[idx] += self_vel
    
    def move_reverse(self) -> None:
        for idx, self_vel in enumerate(self.velocity):
            self.pos[idx] -= self_vel
    
    def __eq__(self, other: 'Moon') -> bool:
        return all(self_p == other_p for self_p, other_p in zip(self.pos, other.pos))

    def energy(self) -> int:
        return sum(map(abs, self.pos)) * sum(map(abs, self.velocity))

    def __repr__(self) -> str:
        return f"Moon(pos={tuple(self.pos)}, vel={tuple(self.velocity)})"

    def __hash__(self):
        return hash(repr(self))

class MoonTracker(object):
    def __init__(self, moons):
        self.moon_tables = []
        self.moons = moons
        self.update_moon_tables()

    def simulate(self):
        weights = {moon: [0,0,0] for moon in self.moons}
        for dim, table in enumerate(self.moon_tables):
            seen = 0
            upcoming = len(self.moons)
            for _, row in sorted(table.items(), key=lambda p: p[0]):
                row_size = len(row)
                upcoming -= row_size
                # is above `upcoming - row_size` moons
                # is below `seen` moons
                for moon in row: 
                    weights[moon][dim] = upcoming - seen
                seen += row_size
        for moon in moons:
            moon.apply_grav(weights[moon])
            moon.move()
        self.update_moon_tables()
    
    def update_moon_tables(self):
        self.moon_tables = [defaultdict(set) for _ in range(3)]
        for moon in self.moons:
            for dim in range(3):
                self.moon_tables[dim][moon.pos[dim]].add(moon)
    
    def __repr__(self):
        return f"MoonTracker([{self.moons}])"
    
# Actual Code
moons = [Moon.parse(line) for line in puzzle_input]
tracker = MoonTracker(moons)
# Can't store these because of how much memory it'll take
# Can't loop through the whole amount: takes something like 3 minutes even if doing nothing
snapshots = set()
steps = 0
while repr(tracker) not in snapshots:
    if steps % 1000000 == 0:
        print(steps)
    snapshots.add(repr(tracker))
    tracker.simulate()
    steps += 1
print(steps)

# Result

