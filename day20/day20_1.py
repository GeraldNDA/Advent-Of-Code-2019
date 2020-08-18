#!/usr/bin/env python3
# Imports
from mapping import Directions, Point

from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=20)
puzzle_input = puzzle.get_input(raw=True)
# puzzle_input = [
# "                   A               ",
# "                   A               ",
# "  #################.#############  ",
# "  #.#...#...................#.#.#  ",
# "  #.#.#.###.###.###.#########.#.#  ",
# "  #.#.#.......#...#.....#.#.#...#  ",
# "  #.#########.###.#####.#.#.###.#  ",
# "  #.............#.#.....#.......#  ",
# "  ###.###########.###.#####.#.#.#  ",
# "  #.....#        A   C    #.#.#.#  ",
# "  #######        S   P    #####.#  ",
# "  #.#...#                 #......VT",
# "  #.#.#.#                 #.#####  ",
# "  #...#.#               YN....#.#  ",
# "  #.###.#                 #####.#  ",
# "DI....#.#                 #.....#  ",
# "  #####.#                 #.###.#  ",
# "ZZ......#               QG....#..AS",
# "  ###.###                 #######  ",
# "JO..#.#.#                 #.....#  ",
# "  #.#.#.#                 ###.#.#  ",
# "  #...#..DI             BU....#..LF",
# "  #####.#                 #.#####  ",
# "YN......#               VT..#....QG",
# "  #.###.#                 #.###.#  ",
# "  #.#...#                 #.....#  ",
# "  ###.###    J L     J    #.#.###  ",
# "  #.....#    O F     P    #.#...#  ",
# "  #.###.#####.#.#####.#####.###.#  ",
# "  #...#.#.#...#.....#.....#.#...#  ",
# "  #.#####.###.###.#.#.#########.#  ",
# "  #...#.#.....#...#.#.#.#.....#.#  ",
# "  #.###.#####.###.###.#.#.#######  ",
# "  #.#.........#...#.............#  ",
# "  #########.###.###.#############  ",
# "           B   J   C               ",
# "           U   P   P               ",
# ]

# puzzle_input = [
# "         A           ",
# "         A           ",
# "  #######.#########  ",
# "  #######.........#  ",
# "  #######.#######.#  ",
# "  #######.#######.#  ",
# "  #######.#######.#  ",
# "  #####  B    ###.#  ",
# "BC...##  C    ###.#  ",
# "  ##.##       ###.#  ",
# "  ##...DE  F  ###.#  ",
# "  #####    G  ###.#  ",
# "  #########.#####.#  ",
# "DE..#######...###.#  ",
# "  #.#########.###.#  ",
# "FG..#########.....#  ",
# "  ###########.#####  ",
# "             Z       ",
# "             Z       ",
# ]

class MazeObject(object):
    def __init__(self, pos=None):
        assert pos is not None
        self.pos = pos
        self.adj = set()
    
    def set_neightbours(self, adj):
        self.adj = set(adj)
    
    def next_pos(self):
        return [pos for pos in self.adj if not isinstance(pos, Wall)]
    
    def __repr__(self):
        return f"{type(self).__name__}(pos={self.pos})"


    @staticmethod
    def to_maze_object(pos, text):
        if text == "#":
            return Wall(pos=pos)
        elif text == ".":
            return Passage(pos=pos)
        elif text.isalpha():
            if text == "AA":
                return Entrance(pos=pos)
            if text == "ZZ":
                return Exit(pos=pos)
            return WarpPoint(text, pos=pos)
        raise ValueError(f"No maze object for {pos, text}")

class Wall(MazeObject):
    def next_pos(self):
        return []

class Passage(MazeObject):
    pass

class WarpPoint(MazeObject):
    def __init__(self, name, **kwargs):
        assert name is not None
        self.name = name
        self.warp_to = None
        super().__init__(**kwargs)

    def set_warp_to(self, other):
        assert isinstance(other, WarpPoint) and other.name == self.name
        self.warp_to = other

    def next_pos(self):
        assert self.warp_to is not None, self
        return [pos for pos in self.warp_to.adj if not isinstance(pos, (Wall, WarpPoint))]

    def __repr__(self):
        return f"WarpPoint(name={self.name}, pos={self.pos})"

class Entrance(MazeObject):
    pass

class Exit(MazeObject):
    def next_pos(self):
        return []

# Actual Code
class Maze(object):
    def __init__(self, maze_map):
        self.maze, self.entrance = Maze.parse_maze(maze_map)
    
    def path_to_exit(self):
        paths = [(self.entrance,)]
        while paths:
            curr_path = paths.pop(0)
            # added = 0
            for pos in curr_path[-1].next_pos():
                if isinstance(pos, Exit):
                    return curr_path + (pos,)
                if pos not in curr_path:
                    paths.append(curr_path + (pos,))
            #         added += 1
            # if not added:
            #     print(curr_path[-1], curr_path[-1].next_pos())
        return tuple()

    @staticmethod
    def parse_maze(maze_map):
        temp_maze = {}
        warp_points = {}
        for row_idx, row in enumerate(puzzle_input):
            for col_idx, elem in enumerate(row):
                curr = Point(x=col_idx, y=row_idx)
                above_letter = Directions.NORTH + curr
                beside_letter = Directions.WEST + curr
                if elem.isalpha():
                    if above_letter in warp_points:
                        text = warp_points[above_letter] + elem
                        temp_maze[curr] = MazeObject.to_maze_object(curr, text)
                        temp_maze[above_letter] = MazeObject.to_maze_object(above_letter, text)
                    elif beside_letter in warp_points:
                        text = warp_points[beside_letter] + elem
                        temp_maze[curr] = MazeObject.to_maze_object(curr, text)
                        temp_maze[beside_letter] = MazeObject.to_maze_object(beside_letter, text)
                    else:
                        warp_points[curr] = elem
                elif elem in "#.":
                    temp_maze[curr] = MazeObject.to_maze_object(curr, elem)
        # Remove duplicates
        maze = {}
        warp_points = {}
        entrance = None
        for pos, elem in temp_maze.items():
            valid_neighbours = [temp_maze.get(d + pos) for d in Directions]
            valid_neighbours = [neighbour for neighbour in valid_neighbours if neighbour is not None]
            if isinstance(elem, (WarpPoint, Entrance, Exit)):
                # only neighbour is self
                if len(valid_neighbours) == 1:
                    continue
            maze[pos] = elem
            elem.set_neightbours(valid_neighbours)
            if isinstance(elem, WarpPoint):
                if elem.name not in warp_points:
                    warp_points[elem.name] = elem
                else:
                    other = warp_points[elem.name]
                    elem.set_warp_to(other)
                    other.set_warp_to(elem)
            if isinstance(elem, Entrance):
                entrance = elem
        # print(warp_points, "AA" in warp_points)
        return maze, entrance
# Result
maze = Maze(puzzle_input)
step_count = 0
for idx, pos in enumerate(maze.path_to_exit()):
    if isinstance(pos, (WarpPoint, Entrance, Exit)):
        print(pos)
        continue
    step_count += 1
    # print(idx, pos)
    # Remove stepping on warp point and stepping off
print(step_count - 1)