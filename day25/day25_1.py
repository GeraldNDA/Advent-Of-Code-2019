#!/usr/bin/env python3
# Imports
import re
from collections import namedtuple, defaultdict
from itertools import combinations

from mapping import Directions, Point
from intcode_parser import IntComputer
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=25)
puzzle_input = puzzle.get_input()

class DroidReader(object):
    WORD = r".+"
    ANY_TEXT = r".+"

    LIST_ELEM = r"(?:- (?:.+)\n)"
    NL = r"\n"
    DROID_RESPONSE = re.compile(
        f"== ({WORD}) =={NL}"
        f"({ANY_TEXT}){NL}{NL}"
        f"Doors here lead:{NL}({LIST_ELEM}+){NL}"
        f"(?:Items here:{NL}({LIST_ELEM}+){NL})?"
        f"Command\\?{NL}?"
        , flags=re.MULTILINE
    )

    LIST_ITEM = re.compile(
        r"- (.+)\n",
        flags=re.MULTILINE
    )

    Response = namedtuple("Response", ("name", "description", "doors", "items"))

    def __init__(self, code, blacklist=None, avoid=None):
        self.input_gen = self.next_dir()
        self.droid = IntComputer(
            code=code,
            inputs=lambda _: next(self.input_gen)
        )
        self.blacklist = blacklist
        self.droid_response = ""
        self.seen = defaultdict(set)
        self.path = []
        self.pos = Point(0,0)
        self.items = []
        self.avoid = avoid or []
    
    def run(self):
        try:
            for _ in self.droid:
                if self.droid.outputs:
                    self.droid_response += chr(self.droid.outputs.pop())
        except AssertionError:
            return self.droid_response
            # return self.droid_response.strip().splitlines()[6]

    def backtrack(self):
        assert self.path
        last_dir = self.path.pop()
        self.pos -= last_dir.value
        for char in last_dir.opposite().name.lower():
            yield ord(char)
        yield ord("\n")

    def pick_all(self, items):
        for item in items:
            if item not in self.blacklist:
                # print("PICK>", item)
                command = "take " + item
                for char in command:
                    yield ord(char)
                yield ord("\n")
                self.items.append(item)


    def next_dir(self):
        while True:
            # print(self.droid_response)
            response = DroidReader.parse(self.droid_response)
            # print(response.name, response.description)

            possible_dirs = set(response.doors)
            possible_dirs.discard(self.path[-1].opposite() if self.path else None)
            possible_dirs -= self.seen[self.pos]

            for char in self.pick_all(response.items):
                yield char
            self.droid_response = ""
            
            if not possible_dirs:
                for char in self.backtrack():
                    yield char
                continue
            
            avoid_dir = self.avoid[len(self.path)] if len(self.path) < len(self.avoid) else None
            new_dir = sorted(possible_dirs, key=lambda d: d is avoid_dir)[0]
            self.path.append(new_dir)
            self.seen[self.pos].add(new_dir)
            self.pos = new_dir + self.pos
        
            # print("MOVE>", new_dir)
            for char in new_dir.name.lower():
                yield ord(char)
            yield ord("\n")


    @staticmethod
    def parse(r):
        response = DroidReader.DROID_RESPONSE.match(r.strip())
        assert response, f"{r.strip()}"
        name = response.group(1)
        description = response.group(2)
        doors = DroidReader.LIST_ITEM.findall(response.group(3)) if response.group(3) else []
        items = DroidReader.LIST_ITEM.findall(response.group(4)) if response.group(4) else []
        doors = [Directions[door.upper()] for door in doors]
        return DroidReader.Response(name=name, description=description, doors=doors, items=items)

item_blacklist = [
    "infinite loop", 
    "photons", 
    "giant electromagnet",
    "molten lava",
    "escape pod"
    ]
avoid = [
    Directions.WEST, Directions.WEST,
    Directions.SOUTH, Directions.SOUTH,
    Directions.EAST, Directions.EAST,
    Directions.NORTH, Directions.NORTH 
]

droid_code = [int(i) for i in puzzle_input.split(",")]
dr = DroidReader(
    code=list(droid_code),
    blacklist=item_blacklist,
    avoid=avoid, 
)

dr.run()
items = set(dr.items)


done = False
# Could be faster if utilized the response infromation to determine which items to keep
# But there are 8 items so it doesn't take too long to just brute force it.
for remove_amount in range(len(items)):
    for to_remove in combinations(items, remove_amount):
        print("COLLECTING", items - set(to_remove))
        dr = DroidReader(
                code=list(droid_code),
                blacklist=item_blacklist + list(to_remove),
                avoid=avoid,
            )
        resp = dr.run()
        if resp is not None:
            continue
        print(dr.droid_response)
        done = True
        break
    if done:
        break