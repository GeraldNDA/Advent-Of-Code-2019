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
    def __init__(self, area):
        self.map, self.width = Eris.from_text(area)
    
    @staticmethod
    def from_text(area):
        eris = [[Tile.from_text(tile) for tile in row] for row in puzzle_input]
        height = len(eris)
        width = len(eris[0])
        for row_idx, row in enumerate(eris):
            for col_idx, tile in enumerate(row):
                p = Point(col_idx, row_idx)
                neighbours = set(d + p for d in Directions if (d + p).in_range(width, height))
                tile.neighbours = [eris[p.y][p.x] for p in neighbours]
        return sum(eris, []), width
            
    def tick(self):
        for tile in self.map:
            tile.get_new_state()
        for tile in self.map:
            tile.tick()
        
    def get_biodiversity(self):
        return sum(tile.is_infested() * (2 ** idx) for idx, tile in enumerate(self.map))

    def __repr__(self):
        planet_map = ""
        for idx, tile in enumerate(self.map):
            planet_map += str(tile)
            if (idx + 1) % self.width == 0:
                planet_map += "\n"
        return planet_map
    
old_layouts = set()
eris = Eris(puzzle_input)
done = False
while not done:
    old_layouts.add(eris.get_biodiversity())
    eris.tick()
    if eris.get_biodiversity() in old_layouts:
        print(eris)
        print(eris.get_biodiversity())
        break
