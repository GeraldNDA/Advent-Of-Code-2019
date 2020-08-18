#!/usr/bin/env python3
# Imports
from mapping import Directions, Point
from collections import namedtuple, defaultdict
from heapq import heappop, heappush


from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=20)
puzzle_input = puzzle.get_input(raw=True)

# puzzle_input = [
#     "         A           ",
#     "         A           ",
#     "  #######.#########  ",
#     "  #######.........#  ",
#     "  #######.#######.#  ",
#     "  #######.#######.#  ",
#     "  #######.#######.#  ",
#     "  #####  B    ###.#  ",
#     "BC...##  C    ###.#  ",
#     "  ##.##       ###.#  ",
#     "  ##...DE  F  ###.#  ",
#     "  #####    G  ###.#  ",
#     "  #########.#####.#  ",
#     "DE..#######...###.#  ",
#     "  #.#########.###.#  ",
#     "FG..#########.....#  ",
#     "  ###########.#####  ",
#     "             Z       ",
#     "             Z       ",
# ] # 26
# puzzle_input = [
#     "                   A               ",
#     "                   A               ",
#     "  #################.#############  ",
#     "  #.#...#...................#.#.#  ",
#     "  #.#.#.###.###.###.#########.#.#  ",
#     "  #.#.#.......#...#.....#.#.#...#  ",
#     "  #.#########.###.#####.#.#.###.#  ",
#     "  #.............#.#.....#.......#  ",
#     "  ###.###########.###.#####.#.#.#  ",
#     "  #.....#        A   C    #.#.#.#  ",
#     "  #######        S   P    #####.#  ",
#     "  #.#...#                 #......VT",
#     "  #.#.#.#                 #.#####  ",
#     "  #...#.#               YN....#.#  ",
#     "  #.###.#                 #####.#  ",
#     "DI....#.#                 #.....#  ",
#     "  #####.#                 #.###.#  ",
#     "ZZ......#               QG....#..AS",
#     "  ###.###                 #######  ",
#     "JO..#.#.#                 #.....#  ",
#     "  #.#.#.#                 ###.#.#  ",
#     "  #...#..DI             BU....#..LF",
#     "  #####.#                 #.#####  ",
#     "YN......#               VT..#....QG",
#     "  #.###.#                 #.###.#  ",
#     "  #.#...#                 #.....#  ",
#     "  ###.###    J L     J    #.#.###  ",
#     "  #.....#    O F     P    #.#...#  ",
#     "  #.###.#####.#.#####.#####.###.#  ",
#     "  #...#.#.#...#.....#.....#.#...#  ",
#     "  #.#####.###.###.#.#.#########.#  ",
#     "  #...#.#.....#...#.#.#.#.....#.#  ",
#     "  #.###.#####.###.###.#.#.#######  ",
#     "  #.#.........#...#.............#  ",
#     "  #########.###.###.#############  ",
#     "           B   J   C               ",
#     "           U   P   P               ",
# ] # No path
# puzzle_input = [
#     "             Z L X W       C                 ",
#     "             Z P Q B       K                 ",
#     "  ###########.#.#.#.#######.###############  ",
#     "  #...#.......#.#.......#.#.......#.#.#...#  ",
#     "  ###.#.#.#.#.#.#.#.###.#.#.#######.#.#.###  ",
#     "  #.#...#.#.#...#.#.#...#...#...#.#.......#  ",
#     "  #.###.#######.###.###.#.###.###.#.#######  ",
#     "  #...#.......#.#...#...#.............#...#  ",
#     "  #.#########.#######.#.#######.#######.###  ",
#     "  #...#.#    F       R I       Z    #.#.#.#  ",
#     "  #.###.#    D       E C       H    #.#.#.#  ",
#     "  #.#...#                           #...#.#  ",
#     "  #.###.#                           #.###.#  ",
#     "  #.#....OA                       WB..#.#..ZH",
#     "  #.###.#                           #.#.#.#  ",
#     "CJ......#                           #.....#  ",
#     "  #######                           #######  ",
#     "  #.#....CK                         #......IC",
#     "  #.###.#                           #.###.#  ",
#     "  #.....#                           #...#.#  ",
#     "  ###.###                           #.#.#.#  ",
#     "XF....#.#                         RF..#.#.#  ",
#     "  #####.#                           #######  ",
#     "  #......CJ                       NM..#...#  ",
#     "  ###.#.#                           #.###.#  ",
#     "RE....#.#                           #......RF",
#     "  ###.###        X   X       L      #.#.#.#  ",
#     "  #.....#        F   Q       P      #.#.#.#  ",
#     "  ###.###########.###.#######.#########.###  ",
#     "  #.....#...#.....#.......#...#.....#.#...#  ",
#     "  #####.#.###.#######.#######.###.###.#.#.#  ",
#     "  #.......#.......#.#.#.#.#...#...#...#.#.#  ",
#     "  #####.###.#####.#.#.#.#.###.###.#.###.###  ",
#     "  #.......#.....#.#...#...............#...#  ",
#     "  #############.#.#.###.###################  ",
#     "               A O F   N                     ",
#     "               A A D   M                     ",
# ] # 396


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

    def depth_delta(self, center):
        # Need to use euclidean distance here
        assert self.warp_to is not None, self
        distance_from_center = sum(map(lambda p: p**2, self.pos - center))
        warp_to_distance_from_center =  sum(map(lambda p: p**2, self.warp_to.pos - center))
        return 1 if distance_from_center < warp_to_distance_from_center else -1


    def __repr__(self):
        return f"WarpPoint(name={self.name}, pos={self.pos})"

class Entrance(MazeObject):
    pass

class Exit(MazeObject):
    def next_pos(self):
        return []

PathState = namedtuple("PathState", ("path", "depth", "length"))

# Actual Code
class Maze(object):

    def __init__(self, maze_map):
        maze, self.entrance, self.exit = Maze.parse_maze(maze_map)
        self.center = sum(maze, Point(0, 0)) // len(maze)

    def path_score(self, state):
        dist_vector = self.exit.pos - state.path[-1].pos
        return (state.depth + 1) * (abs(dist_vector.x) + abs(dist_vector.y))

    @staticmethod
    def get_warps(path):
        warps = []
        last_warp_idx = -1
        for idx, elem in enumerate(path):
            if isinstance(elem, WarpPoint):
                warps.append(elem.name)
                last_warp_idx = idx
        return warps, last_warp_idx

    def has_no_cycles(self, path):
        # last element will be new pos
        last_warp_idx = -1
        warp_at_depth = defaultdict(tuple)
        # Find all warps and warps similar warps if last is a warp
        depth = 0
        for idx, elem in enumerate(path):
            if isinstance(elem, WarpPoint):
                depth += elem.depth_delta(self.center)
                if depth in warp_at_depth[elem]:
                    return False
                warp_at_depth[elem] += (depth,)
                if elem != path[-1]:
                    last_warp_idx = idx
        if last_warp_idx >= 0 and isinstance(path[-1], WarpPoint) and path[-1].name == path[last_warp_idx].name:
            return False
        return path[-1] not in path[last_warp_idx+1:-1]

    def path_to_exit(self):
        score_counts = defaultdict(int)
        start_state = PathState(
            path=(self.entrance,),
            depth=0,
            length=0
        )
        start_score = self.path_score(start_state)
        score_counts[start_score] += 1
        paths = [(start_score, score_counts[start_score], start_state)]
        while paths:
            curr_score, _, curr_path = heappop(paths)
            print(f"score={curr_score:>5} length={curr_path.length:>5}", end="\r")
            for pos in curr_path.path[-1].next_pos():
                if isinstance(pos, Exit):
                    # print(f"FOUND EXIT {curr_path.depth} {curr_path.length}")
                    if not curr_path.depth:
                        print(curr_path.length)
                        return PathState(
                            path=curr_path.path + (pos,),
                            depth=curr_path.depth,
                            length=curr_path.length
                        )
                    continue

                new_depth = curr_path.depth
                is_warp = isinstance(pos, WarpPoint)
                if is_warp:
                    new_depth += pos.depth_delta(self.center)
                if new_depth < 0:
                    continue

                if self.has_no_cycles(curr_path.path + (pos,)):
                    new_path = PathState(
                        path=curr_path.path + (pos,),
                        depth=new_depth,
                        length=curr_path.length + int(not is_warp),
                    )
                    new_path_score = self.path_score(new_path)
                    score_counts[new_path_score] += 1
                    heappush(paths, (new_path_score, score_counts[new_path_score], new_path))
        raise ValueError("No path found")

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
        map_exit = None
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
            if isinstance(elem, Exit):
                map_exit = elem
        # print(warp_points, "AA" in warp_points)
        return maze, entrance, map_exit

# Result
maze = Maze(puzzle_input)
maze_path = maze.path_to_exit()
print()
print(maze_path.length - 1, maze_path.depth)