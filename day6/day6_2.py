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
#     "K)YOU",
#     "I)SAN",
# ]
# shuffle(puzzle_input)

# Actual Code
orbit_checksum = 0
orbits = defaultdict(set)
reverse_orbits = defaultdict(lambda: None)
for orbiter, orbitee in (relationship.split(")") for relationship in puzzle_input):
    orbits[orbiter].add(orbitee)
    assert reverse_orbits[orbitee] is None
    reverse_orbits[orbitee] = orbiter
depth_map = {}
curr_orbiters = {"COM",}
depth = 0
while curr_orbiters:
    orbitees = set()
    for orbiter in curr_orbiters:
        depth_map[orbiter] = depth
        orbitees |= orbits[orbiter]
    depth += 1 
    curr_orbiters = orbitees  

you_object = "YOU"
santa_object = "SAN"
while you_object != santa_object:
    you_depth = depth_map[you_object]
    santa_depth = depth_map[santa_object]
    if you_depth >= santa_depth:
        you_object = reverse_orbits[you_object]
    if you_depth < santa_depth:
        santa_object = reverse_orbits[santa_object]
common_parent_depth = depth_map[santa_object]
print(common_parent_depth)

# Result
print(depth_map["YOU"] + depth_map["SAN"] - 2*(common_parent_depth + 1))
# print(orbits)