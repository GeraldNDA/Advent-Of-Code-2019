#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode
from math import gcd, degrees, atan2
from itertools import combinations

# Input Parse
puzzle = AdventOfCode(year=2019, day=10)
puzzle_input = puzzle.get_input()
# puzzle_input = [
# ".#..##.###...#######",
# "##.############..##.",
# ".#.######.########.#",
# ".###.#######.####.#.",
# "#####.##.#.##.###.##",
# "..#####..#.#########",
# "####################",
# "#.####....###.#.#.##",
# "##.#################",
# "#####.##.###..####..",
# "..######..##.#######",
# "####.##.####...##..#",
# ".#####..#.######.###",
# "##...#.##########...",
# "#.##########.#######",
# ".####.#.###.###.#.##",
# "....##.##.###..#####",
# ".#.#.###########.###",
# "#.#.#.#####.####.###",
# "###.##.####.##.#..##",

# ]

# Actual Code
class Point(object):

    __slots__ = ["x", "y"]

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __neg__(self) -> 'Point':
        return Point(-self.x, -self.y)

    def __sub__(self, other: 'Point') -> 'Point':
        return self + (-other)

    def __add__(self, other: 'Point') -> 'Point':
        return Point(self.x + other.x, self.y + other.y)

    def __floordiv__(self, other):
        return Point(self.x // other, self.y // other)


    def __eq__(self, other: 'Point') -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    @staticmethod
    def dot(p1: 'Point', p2: 'Point') -> int:
        return p1.x * p2.x + p1.y * p2.y

    @staticmethod
    def det(p1: 'Point',  p2: 'Point') -> int:
        return p1.x * p2.y - p1.y * p2.x

    def angle_with_vertical(self, other: 'Point') -> int:
        vertical = Point(x=self.x, y=0) - self
        to_other = other - self
        dot = Point.dot(vertical, to_other)
        det = Point.det(vertical, to_other)
        angle = degrees(atan2(det, dot))
        while angle < 0:
            angle += 360
        return angle

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

def in_between_points(asteroid1: Point, asteroid2: Point):
    dist = asteroid2 - asteroid1
    divisor = gcd(dist.x, dist.y)
    dist //= divisor
    point = asteroid1 + dist
    while point != asteroid2:
        yield point
        point += dist 

asteroids = {}
for row_idx, row in enumerate(puzzle_input):
    for col_idx, obj in enumerate(row):
        if obj == "#":
            asteroids[Point(x=col_idx, y=row_idx)] = set()

for asteroid_pair in combinations(asteroids, 2):
    for point in in_between_points(*asteroid_pair):
        if point in asteroids:
            break
    else:
        asteroid1, asteroid2 = asteroid_pair
        asteroids[asteroid1].add(asteroid2)
        asteroids[asteroid2].add(asteroid1)

station = max(asteroids, key=lambda a: len(asteroids[a]))
print(f"Station is at {station}")
# Spin laser
# Only requires 1 spin since 384 asteroids found in part 1 (otherwise would have to spin and search again)
for idx, asteroid in enumerate(sorted(asteroids[station], key=lambda a: station.angle_with_vertical(a)), start=1):
    if idx == 200:
        print(asteroid)
        break


# Result
# for a in asteroids:
#     print( a, asteroids[a])