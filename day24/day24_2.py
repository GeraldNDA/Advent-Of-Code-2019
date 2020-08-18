#!/usr/bin/env python3
# Imports
from enum import Enum
from operator import add

from mapping import Point, Directions
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=24)
puzzle_input = puzzle.get_input()
# puzzle_input = [
#     "....#",
#     "#..#.",
#     "#..##",
#     "..#..",
#     "#....",
# ]
# Actual Code
class TileState(Enum):
    INFESTED = "#"
    EMPTY = "."
    def opposite(self):
        if self is TileState.INFESTED:
            return TileState.EMPTY
        return TileState.INFESTED

class Tile(object):

    def __init__(self, initial_state):
        self.state = initial_state
        self.new_state = None
        self.neighbours = []
    
    @staticmethod
    def from_text(text):
        tile  = None
        if text == "#":
            tile = Tile(TileState.INFESTED)
        if text == ".":
            tile = Tile(TileState.EMPTY)
        assert tile
        return tile
    
    def get_new_state(self):
        infested_neighbours = sum(neighbour.is_infested() for neighbour in self.neighbours)
        self.new_state = self.state
        if self.is_infested():
            if infested_neighbours != 1:
                self.new_state = self.state.opposite()
        else:
            if 1 <= infested_neighbours <= 2:
                self.new_state = self.state.opposite()
        
    def add_neighbour(self, tile):
        self.neighbours.append(tile)
        tile.neighbours.append(self)

    def tick(self):
        self.state = self.new_state
        self.new_state = None

    def is_infested(self):
        return self.state is TileState.INFESTED
    
    def __str__(self):
        return "#" if self.is_infested() else "."
    
    def __repr__(self):
        return f"Tile(state={str(self)})"
    


class Eris(object):
    def __init__(self, area, depth=0, empty=False):
        self.raw_map = area
        self.depth = depth
        self.map, self.width = Eris.from_text(self.raw_map, empty=empty)
        self.larger_map = None
        self.smaller_map = None
    
    def get_tile(self, point):
        assert point.in_range(self.width, self.width), f"{point}"
        return self.map[point.y][point.x]

    @staticmethod
    def add_new_neighbours(larger_map, smaller_map, width):
        center_idx = width // 2
        center = Point(center_idx, center_idx)
        center_tile = larger_map.get_tile(center)
        for direction in Directions:
            neighbour = larger_map.get_tile(direction + center)
            neighbour.neighbours.remove(center_tile)
            major_orientation = bool(direction.value.y)
            major_dim_index = direction.value.y if major_orientation else direction.value.x
            major_dim_index = 0 if major_dim_index < 0 else width-1
            increment_dir = Point(1, 0) if major_orientation else Point(0, 1)
            base_pos = Point(0, major_dim_index) if major_orientation else Point(major_dim_index, 0)
            for idx in range(width):
                new_neighbour = smaller_map.get_tile(base_pos + idx*increment_dir)
                new_neighbour.add_neighbour(neighbour)

    def any_outer_infected(self):
        for direction in Directions:
            major_orientation = bool(direction.value.y)
            major_dim_index = direction.value.y if major_orientation else direction.value.x
            major_dim_index = 0 if major_dim_index < 0 else self.width-1
            increment_dir = Point(1, 0) if major_orientation else Point(0, 1)
            base_pos = Point(0, major_dim_index) if major_orientation else Point(major_dim_index, 0)
            for idx in range(self.width):
                if self.get_tile(base_pos + idx*increment_dir).is_infested():
                    return True
        return False

    def any_inner_infected(self):
        return any(n.is_infested() for n in self.get_center().neighbours)

    def do_recurse(self):
        if not self.larger_map and self.any_outer_infected():
            self.larger_map = Eris(self.raw_map, self.depth - 1, empty=True)
            self.larger_map.smaller_map = self
            Eris.add_new_neighbours(self.larger_map, self, width=self.width)
        if not self.smaller_map and self.any_inner_infected():
            self.smaller_map = Eris(self.raw_map, self.depth + 1, empty=True)
            self.smaller_map.larger_map = self
            Eris.add_new_neighbours(self, self.smaller_map, width=self.width)
        
        if self.should_recurse_up():
            self.larger_map.do_recurse()
        if self.should_recurse_down():
            self.smaller_map.do_recurse()

    def get_center(self):
        assert self.width == len(self.map) and self.width % 2
        center = self.width // 2
        return self.map[center][center]



    @staticmethod
    def from_text(area, empty=False):
        if empty:
            area = [row.replace("#", ".") for row in area]
        eris = [[Tile.from_text(tile) for tile in row] for row in area]
        height = len(eris)
        width = len(eris[0])
        for row_idx, row in enumerate(eris):
            for col_idx, tile in enumerate(row):
                p = Point(col_idx, row_idx)
                neighbours = set(d + p for d in Directions if (d + p).in_range(width, height))
                tile.neighbours = [eris[p.y][p.x] for p in neighbours]
        return eris, width
    
    def count_infested(self):
        infested = 0
        if self.should_recurse_up():
            infested += self.larger_map.count_infested()
        infested += sum(t.is_infested() for t in sum(self.map, []) if t is not self.get_center())
        if self.should_recurse_down():
            infested += self.smaller_map.count_infested()
        return infested

    def should_recurse_down(self):
        return self.smaller_map and self.depth >= 0
        
    def should_recurse_up(self):
        return self.larger_map and self.depth <= 0

    def calculate_states(self):
        flat_map = sum(self.map, [])
        # Order doesn't matter
        if self.should_recurse_up():
            self.larger_map.calculate_states()
        for tile in flat_map:
            tile.get_new_state()
        if self.should_recurse_down():
            self.smaller_map.calculate_states()

    def update_states(self):
        flat_map = sum(self.map, [])
        if self.should_recurse_up():
            self.larger_map.update_states()
        for tile in flat_map:
            tile.tick()
        if self.should_recurse_down():
            self.smaller_map.update_states()


    def tick(self):
        self.do_recurse()
        self.calculate_states()
        self.update_states()

    def __repr__(self):
        flat_map = sum(self.map, [])
        planet_map = ""
        if self.should_recurse_up():
            planet_map += f"{self.larger_map}=====\n"
        for idx, tile in enumerate(flat_map):
            planet_map += str(tile)
            if (idx + 1) % self.width == 0:
                planet_map += "\n"
        if self.should_recurse_down():
            planet_map += f"=====\n{self.smaller_map}\n"
        return planet_map
    
old_layouts = set()
eris = Eris(puzzle_input)
print(eris)
for _ in range(200):
    eris.tick()
# eris.tick()
# print("*"*30)

# print(eris)
print(eris.count_infested())
# done = False
# MAX_TIME = 200
# for _ in range(MAX_TIME):
#     eris.tick()
#     eris
#     break
