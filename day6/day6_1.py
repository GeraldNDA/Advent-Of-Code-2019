#!/usr/bin/env python3
# Imports


from collections import defaultdict
from random import shuffle

from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=6)
puzzle_input = puzzle.get_input()
# puzzle_input = [
#     "COM)B",
#     "B)C",
#     "C)D",
#     "D)E",
#     "E)F",
#     "B)G",
#     "G)H",
#     "D)I",
#     "E)J",
#     "J)K",
#     "K)L",
# ]
# shuffle(puzzle_input)

# Actual Code
orbit_checksum = 0
orbits = defaultdict(set)
for orbiter, orbitee in (relationship.split(")") for relationship in puzzle_input):
    orbits[orbiter].add(orbitee)
curr_orbiters = {"COM",}
depth = 0
while curr_orbiters:
    orbitees = set()
    for orbiter in curr_orbiters:
        orbit_checksum += depth
        orbitees |= orbits[orbiter]
    depth += 1 
    curr_orbiters = orbitees  

# Result
print(orbit_checksum)
# print(orbits)