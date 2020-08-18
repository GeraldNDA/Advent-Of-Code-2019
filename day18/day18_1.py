#!/usr/bin/env python3
# Imports
from enum import Enum
from itertools import combinations
from collections import defaultdict, namedtuple, OrderedDict
from math import inf

from mapping import Directions, Point
from aoc import AdventOfCode


# Input Parse
puzzle = AdventOfCode(year=2019, day=18)
puzzle_input = puzzle.get_input()

# puzzle_input = [
#     "#########",
#     "#b.A.@.a#",
#     "#########",
# ]
# puzzle_input = [
#     "########################",
#     "#f.D.E.e.C.b.A.@.a.B.c.#",
#     "######################.#",
#     "#d.....................#",
#     "########################",
# ] # 86
# puzzle_input = [
#     "########################",
#     "#...............b.C.D.f#",
#     "#.######################",
#     "#.....@.a.B.c.d.A.e.F.g#",
#     "########################",
# ] # 132
# puzzle_input = [
#     "#################",
#     "#i.G..c...e..H.p#",
#     "########.########",
#     "#j.A..b...f..D.o#",
#     "########@########",
#     "#k.E..a...g..B.n#",
#     "########.########",
#     "#l.F..d...h..C.m#",
#     "#################",
# ] # 136
# puzzle_input = [
#     "########################",
#     "#@..............ac.GI.b#",
#     "###d#e#f################",
#     "###A#B#C################",
#     "###g#h#i################",
#     "########################",
# ] # 81

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

class Vault(object):
    PathElement = namedtuple("PathElement", ("pos", "collected", "doors"))

    def __init__(self, scan):
        self.vault_map = {}
        self.keys = {}
        curr_pos = None
        for y, line in enumerate(scan):
            for x, element in enumerate(line):
                if element.isalpha():
                    element = Door(element) if element.isupper() else Key(element)
                else:
                    element = MapElement(element)
                if element is MapElement.ENTRANCE:
                    curr_pos = Point(x, y)
                if isinstance(element, Key):
                    self.keys[element] = Point(x, y)
                    
                self.vault_map[Point(x, y)] = element
        self.vault_map[curr_pos] = MapElement.OPEN_PASSAGE
        self.start = curr_pos

    def find_path_to(self, key, start=None):
        start = start or self.start
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
        raise ValueError(f"Couldn't find a path from {start} => {key} using collected keys")
    
    def distance_to_others(self, collected):
        start_pos = collected[-1] if collected else None
        start_pos = self.keys[start_pos] if start_pos else self.start
        total_distance = 0
        for key, key_pos in self.keys.items():
            if key in collected:
                continue
            total_distance += sum((key_pos - start_pos).abs())
        return total_distance

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
key_distances = {}
sorted_key_list = sorted(vault.keys, key=str)
KeyRelationship = namedtuple("KeyRelationship", ("distance", "doors_required", "keys_collected"))
for idx, key in enumerate(sorted_key_list):
    print(len(sorted_key_list) - idx - 1, "remaining")
    # From start to key
    path = vault.find_path_to(key)
    assert key == path[-1].collected[-1]
    key_distances[(None, key)] = KeyRelationship(len(path), path[-1].doors, path[-1].collected)
    # from other_key to key
    for other_key in sorted_key_list[idx+1:]:
        path = vault.find_path_to(key, start=vault.keys[other_key])
        other_collected = path[-1].collected[-2::-1]
        other_collected += (other_key,)
        assert key == path[-1].collected[-1], f"{key}, {path[-1].collected}"
        assert other_key == other_collected[-1], f"{other_key}, {path[-1].collected}  => {other_collected}"
        key_distances[(key, other_key)] = KeyRelationship(len(path), path[-1].doors, other_collected)
        key_distances[(other_key, key)] = KeyRelationship(len(path), path[-1].doors, path[-1].collected)

print(f"Found {len(key_distances)} distances for {len(vault.keys)}")
PathInfo = namedtuple("PathInfo", ("distance", "path"))
def find_path_through(previous_paths):
    print()
    top = previous_paths.pop()
    top_is_key =  isinstance(top, Key)
    previous_paths.add(top)
    new_previous_paths = set()
    if top_is_key:
        
        return find_path_through(new_previous_paths)
    prev_path_len = len(top.path)
    if prev_path_len == len(vault.keys):
        return min(previous_paths, key=lambda p: p.distance)
    for key in vault.keys:
        best_path = None
        for prev_path in previous_paths:
            if key in prev_path.path:
                continue
            distance_info = key_distances[prev_path.path[-1], key]
            if distance_info.doors_required - set(prev_path.path):
                continue
            new_distance = distance_info.distance + prev_path.distance - 1
            if best_path is None or best_path.distance > new_distance:
                best_path = PathInfo(
                    distance=new_distance,
                    path=prev_path.path + (key,)
                )
        if best_path is not None:
            print(best_path)
            new_previous_paths.add(best_path)

    return find_path_through(new_previous_paths)

# print(find_path_through(set(vault.keys)))

path_info = {}
def build_path_info():
    for key in vault.keys:
        distance_info = key_distances[(None, key)]
        if distance_info.doors_required:
            continue
        path_info[(key,), key] = PathInfo(
            distance=distance_info.distance - 1,
            path=(key,)
        )

    for set_size in range(2, len(vault.keys) + 1):
        print(f"SET SIZE={set_size}")
        for curr_set in combinations(vault.keys, set_size):
            for next_key in curr_set:
                subset = tuple(sorted(set(curr_set) - {next_key}, key=str))
                for end_key in set(vault.keys) - {next_key}:
                    if (subset, end_key) not in path_info:
                        continue
                    distance_info = key_distances[(end_key, next_key)]
                    if distance_info.doors_required - set(subset):
                        continue
                    superset = tuple(sorted(subset + (next_key,), key=str))
                    new_distance = distance_info.distance + path_info[subset, end_key].distance - 1
                    if path_info.get((superset, next_key), PathInfo(inf, None)).distance > new_distance:
                        path_info[superset, next_key] = PathInfo(
                            distance=new_distance,
                            path=path_info[subset, end_key].path + (next_key,)
                        )
sorted_key_tuple = tuple(sorted_key_list)
# print(f"min_distance={min((path_info.get((sorted_key_tuple, key), PathInfo(inf, None)) for key in vault.keys), key=lambda p: p.distance)}")

def update_path_info(prev_sets):
    if not prev_sets:
        for last_key in vault.keys:
            distance_info = key_distances[None, last_key]
            if distance_info.doors_required:
                continue
            path_info[(last_key,), last_key] = PathInfo(
                distance=distance_info.distance - 1,
                path=(last_key,)
            )
            yield (last_key,), last_key

    for prev_set, last_key in prev_sets:
        for following_key in set(vault.keys) - set(prev_set):
            distance_info = key_distances[last_key, following_key]
            if distance_info.doors_required - set(prev_set):
                continue
            next_set = tuple(sorted(prev_set + (following_key,), key=str))
            new_distance = distance_info.distance + path_info[prev_set, last_key].distance - 1
            if path_info.get((next_set, following_key), PathInfo(inf, None)).distance > new_distance:
                path_info[next_set, following_key] = PathInfo(
                    distance=new_distance,
                    path=path_info[prev_set, last_key].path + (following_key,)
                )
            yield next_set, following_key

curr_sets = {}
set_size = 0
while set_size < len(vault.keys):
    curr_sets = set(update_path_info(curr_sets))
    set_size += 1
    print(f"SET_SIZE = {set_size}, {len(curr_sets)}")
print(f"min_distance={min(map(lambda curr_set: path_info[curr_set], curr_sets), key=lambda p: p.distance)}")

