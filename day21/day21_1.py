#!/usr/bin/env python3
# Imports
from intcode_parser import IntComputer

from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=21)
puzzle_input = puzzle.get_input()

# Actual Code
class SpringBot(object):
    MAX_ASCII = 1 << 8
    def __init__(self, parser, script):
        self.script = script
        self.script_input = self.script_reader()
        self.parser = IntComputer(
            code=parser,
            inputs=self.feed_script
        )

    def script_reader(self):
        for line in self.script:
            for char in line:
                yield ord(char)
            yield ord("\n")

    def feed_script(self, _):
        return next(self.script_input)

    def run(self):
        for _ in self.parser:
            if len(self.parser.outputs):
                output = self.parser.outputs.pop()
                if output > SpringBot.MAX_ASCII:
                    print("Hull Damage:", output)
                else:
                    print(chr(output), end="")

parser_code = [int(i) for i in puzzle_input.split(",")]
# Second param must be T J
# Ops: AND, OR, NOT
# 15 instructions max (not including WALK)
# A - 1, B - 2, C - 3, D - 4

script = [
    "OR A T",
    "AND B T",
    "AND C T",
    "NOT D J",
    "OR T J",
    "NOT J J",
    "WALK"
]
# if !((A & B & C) | !D):
#     jump
bot = SpringBot(parser=parser_code, script=script)



# Result
bot.run()