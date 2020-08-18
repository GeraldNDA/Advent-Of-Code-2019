#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode
from math import gcd
from itertools import combinations

# Input Parse
puzzle = AdventOfCode(year=2019, day=10)
puzzle_input = puzzle.get_input()
# puzzle_input = [
#     ".#..#",
#     ".....",
#     "#####",
#     "....#",
#     "...##",

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
            asteroids[Point(x=col_idx, y=row_idx)] = 0

for asteroid_pair in combinations(asteroids, 2):
    for point in in_between_points(*asteroid_pair):
        if point in asteroids:
            break
    else:
        asteroids[asteroid_pair[0]] += 1
        asteroids[asteroid_pair[1]] += 1


# Result
best_point = max(asteroids, key=lambda a: asteroids[a])
print(best_point, asteroids[best_point])
# for a in asteroids:
#     print( a, asteroids[a])