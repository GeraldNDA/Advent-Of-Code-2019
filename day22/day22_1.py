#!/usr/bin/env python3
# Imports
import re
from math import gcd
from aoc import AdventOfCode

# NOTE: Had to change algorithm to match part 2, in order to test
# Input Parse
puzzle = AdventOfCode(year=2019, day=22)
puzzle_input = puzzle.get_input()

class Deck(object):
    SHUFFLE_TECHNIQUES = {
        r"deal into new stack": "stack_deal",
        r"cut (-?\d+)": "cut", 
        r"deal with increment (-?\d+)": "increment_deal", 
    }

    def __init__(self, num_cards):
        self.num_cards = num_cards
        self.prod_coeff = 1
        self.add_coeff = 0

    def stack_deal(self):
        # new_idx = -(last_idx + 1) % num_cards
        #         =  -last_idx - 1
        self.prod_coeff *= (-1)
        self.add_coeff *= (-1)
        self.add_coeff -= 1
        # self.add_coeff %= self.num_cards
        # self.prod_coeff %= self.num_cards

    def cut(self, n):
        # new_idx = (last_idx - n) % num_cards
        self.add_coeff -= n
        # self.add_coeff %= self.num_cards

    def increment_deal(self, n):
        # new_idx = curr_idx * n % num_cards
        self.prod_coeff *= n
        self.add_coeff *= n
        # self.add_coeff %= self.num_cards
        # self.prod_coeff %= self.num_cards

    def shuffle(self, shuffle_instructions):
        for instruction in shuffle_instructions:
            for technique, callback in Deck.SHUFFLE_TECHNIQUES.items():
                match = re.fullmatch(technique, instruction)
                if match is not None:
                    callback = getattr(self, callback)
                    callback(*map(int, match.groups()))
                    break
            else:
                raise ValueError(f"No matches for {instruction}")

    def find_card(self, card_number):
        # Finds (a*i + b) % N
        return (self.add_coeff + self.prod_coeff*card_number) % self.num_cards

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.add_coeff, self.prod_coeff) == (other.add_coeff, other.prod_coeff)

# Actual Code
deck = Deck(num_cards=10007)
deck.shuffle(puzzle_input)
print(deck.find_card(2019))
