#!/usr/bin/env python3
# Imports
from enum import Enum
from itertools import combinations
from collections import defaultdict, namedtuple, OrderedDict
from math import inf

from mapping import Directions, Point, Turn
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=18)
puzzle_input = puzzle.get_input()

# puzzle_input = [
#     "#######",
#     "#a.#Cd#",
#     "##...##",
#     "##.@.##",
#     "##...##",
#     "#cB#Ab#",
#     "#######"
# ] # 8
# puzzle_input = [
#     "###############",
#     "#d.ABC.#.....a#",
#     "######...######",
#     "######.@.######",
#     "######...######",
#     "#b.....#.....c#",
#     "###############",
# ] # 24

# Solve
class MapElement(Enum):
    ENTRANCE = "@"
    OPEN_PASSAGE = "."
    STONE_WALL = "#"

    def __str__(self):
        return self.value

class Clearable(object):
    def __init__(self, key_type):
        self.type = key_type.lower()
    
    def __eq__(self, other):
        if not isinstance(other, Clearable):
            return False
        return other.type == self.type
    
    def __hash__(self):
        return hash(self.type)
    
    def __repr__(self):
        return f"{type(self).__name__}({self.type})"

class Key(Clearable):
    def __str__(self):
        return self.type

class Door(Clearable):
    def __str__(self):
        return self.type.upper()
    
    def get_key(self):
        return Key(self.type)

class Entrance:
    def __init__(self, corner):
        self.corner = corner

    def __str__(self):
        return f"Entrance({corner.x}, {corner.y})"

    def __hash__(self):
        return hash(self.corner)

class Vault(object):
    PathElement = namedtuple("PathElement", ("pos", "collected", "doors"))

    def __init__(self, scan):
        self.vault_map = {}
        self.keys = {}
        self.entrances = {}
        entrance = None
        for y, line in enumerate(scan):
            for x, element in enumerate(line):
                if element.isalpha():
                    element = Door(element) if element.isupper() else Key(element)
                else:
                    element = MapElement(element)
                if element is MapElement.ENTRANCE:
                    entrance = Point(x, y)
                if isinstance(element, Key):
                    self.keys[element] = Point(x, y)
                self.vault_map[Point(x, y)] = element

        self.vault_map[entrance] = MapElement.STONE_WALL
        for direction in Directions:
            self.vault_map[direction + entrance] = MapElement.STONE_WALL
            entrance_elem = Entrance(direction + Turn.RIGHT)
            entrance_pos = direction + entrance + entrance_elem.corner
            self.entrances[entrance_elem] = entrance_pos

    def find_path_to(self, key, start=None):
        assert start is not None
        # print(self.vault_map[start], key)
        curr_wave = [[Vault.PathElement(pos=start, collected=tuple(), doors=frozenset())]]
        seen = set()
        key_pos = self.keys[key]
        while curr_wave:
            curr_path = curr_wave.pop()
            curr_step = curr_path[-1]
            seen.add(curr_step.pos)
            for direction in Directions:
                new_pos = direction + curr_step.pos
                elem = self.vault_map[new_pos]
                newly_collected = curr_step.collected
                new_doors = curr_step.doors
                if elem is MapElement.STONE_WALL:
                    continue
                if new_pos in seen:
                    continue
                if isinstance(elem, Door):
                    # 'collect' doors to use later
                    new_doors = new_doors | {elem}
                if isinstance(elem, Key) and elem not in newly_collected:
                    newly_collected += (elem,)
                    if elem == key:
                        return curr_path + [Vault.PathElement(pos=new_pos, collected=newly_collected, doors=new_doors)]
                curr_wave.append(curr_path + [Vault.PathElement(pos=new_pos, collected=newly_collected, doors=new_doors)])
            curr_wave.sort(key=lambda p: sum((p[-1].pos - key_pos).abs()))
        return None

    def __repr__(self):
        max_x = 0
        max_y = 0
        for p in self.vault_map:
            max_x = max(p.x, max_x)
            max_y = max(p.y, max_y)
        vault = ""
        for y in range(0, max_y+1):
            for x in range(0, max_x+1):
                vault += str(self.vault_map[Point(x, y)])
            vault += "\n"
        vault += "="*max_x
        return vault



# Result
vault = Vault(puzzle_input)
# print(vault)
key_distances = {}
sorted_key_list = sorted(vault.keys, key=str)
KeyRelationship = namedtuple("KeyRelationship", ("distance", "doors_required", "keys_collected"))
for idx, key in enumerate(sorted_key_list):
    print(len(sorted_key_list) - idx - 1, "remaining")
    # From start to key
    for entrance, entrance_pos in vault.entrances.items():
        path = vault.find_path_to(key, start=entrance_pos)
        if path is None:
            continue
        key_distances[entrance, key] = KeyRelationship(len(path), path[-1].doors, path[-1].collected)
    # from other_key to key
    for other_key in sorted_key_list[idx+1:]:
        path = vault.find_path_to(key, start=vault.keys[other_key])
        if path is None:
            continue
        other_collected = path[-1].collected[-2::-1]
        other_collected += (other_key,)
        assert key == path[-1].collected[-1], f"{key}, {path[-1].collected}"
        assert other_key == other_collected[-1], f"{other_key}, {path[-1].collected}  => {other_collected}"
        key_distances[(key, other_key)] = KeyRelationship(len(path), path[-1].doors, other_collected)
        key_distances[(other_key, key)] = KeyRelationship(len(path), path[-1].doors, path[-1].collected)

print(f"Found {len(key_distances)} distances for {len(vault.keys)}")


PathInfo = namedtuple("PathInfo", ("distance", "path"))
PathState = namedtuple("PathState", ("seen_keys", "bot_state"))
empty_state = PathState(
    seen_keys=tuple(),
    bot_state=tuple(vault.entrances)
)
default_path = PathInfo(
    distance=inf,
    path=None
)
path_info = {empty_state: PathInfo(distance=0, path=tuple())}

def update_path_info(prev_states):
    for prev_state in prev_states:
        for prev_key in prev_state.bot_state:
            for following_key in set(vault.keys) - set(prev_state.seen_keys):
                if (prev_key, following_key) not in key_distances:
                    continue
                distance_info = key_distances[prev_key, following_key]
                if distance_info.doors_required - set(prev_state.seen_keys):
                    continue
                next_state = PathState(
                    seen_keys=tuple(sorted(prev_state.seen_keys + (following_key,), key=str)),
                    bot_state=tuple(following_key if prev_key is other_key else other_key for other_key in prev_state.bot_state)
                )
                new_distance = distance_info.distance + path_info[prev_state].distance - 1
                if path_info.get(next_state, default_path).distance > new_distance:
                    path_info[next_state] = PathInfo(
                        distance=new_distance,
                        path=path_info[prev_state].path + (following_key,)
                    )
                yield next_state

curr_states = {empty_state}
set_size = 0
while set_size < len(vault.keys):
    curr_states = set(update_path_info(curr_states))
    set_size += 1
    print(f"SET_SIZE = {set_size}, {len(curr_states)}")
print(f"min_distance={min(map(lambda curr_state: path_info[curr_state], curr_states), key=lambda p: p.distance)}")

