from enum import Enum

class Point(object):
    __slots__ = ["x", "y"]

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __neg__(self) -> 'Point':
        return Point(-self.x, -self.y)

    def abs(self) -> 'Point':
        return Point(abs(self.x), abs(self.y))

    def __sub__(self, other) -> 'Point':
        if not isinstance(other, (Point, int)):
            return NotImplemented
        return self + (-other)

    def __add__(self, other) -> 'Point':
        if isinstance(other, Point):
            return Point(self.x + other.x, self.y + other.y)
        if isinstance(other, int):
            return Point(self.x + other, self.y + other)
        else:
            return NotImplemented

    def __mul__(self, other) -> 'Point':
        if isinstance(other, int):
            return Point(self.x * other, self.y * other)
        if isinstance(other, Point):
            return Point(self.x * other.x, self.y * other.y)
        else:
            return NotImplemented
        
    def __rmul__(self, other) -> 'Point':
        return self * other

    def __eq__(self, other: 'Point') -> bool:
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"
    
    def __iter__(self):
        yield from (self.x, self.y)

    def in_range(self, width: int, height: int) -> bool:
        return 0 <= self.x < width and 0 <= self.y < height 

Turn = Enum("Turn", ["RIGHT", "LEFT"])    

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

    def __add__(self, other: 'Point') -> 'Point':
        if isinstance(other, Turn):
            return self.turn(other)
        return self.value + other
    
    def __radd__(self, other: 'Point') -> 'Point':
        if isinstance(other, Turn):
            return self.turn(other)
        return self.value + other
    
    def turn(self, turn_dir):
        point = self.value
        if turn_dir is Turn.RIGHT:
            return Directions(Point(-point.y, point.x))

        if turn_dir is Turn.LEFT:
            return Directions(Point(point.y, point.x))

        raise ValueError("Invalid turn direction")