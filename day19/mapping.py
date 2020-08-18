from enum import Enum

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

    def __eq__(self, other: 'Point') -> bool:
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
    
    def in_image(self, width, height):
        return 0 <= self.x < width and 0 <= self.y < height 

class Directions(Enum):
    NORTH = Point(0, -1)
    SOUTH = Point(0, +1)
    WEST = Point(-1, 0)
    EAST = Point(+1, 0)

    def opposite(self):
        point = self.value
        return Directions(-point)

    def movement_command(self):
        if self is Directions.NORTH:
            return 1
        elif self is Directions.SOUTH:
            return 2
        elif self is Directions.WEST:
            return 3
        elif self is Directions.EAST:
            return 4
