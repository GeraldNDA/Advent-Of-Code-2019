#!/usr/bin/env python3
# Imports
import re
from math import gcd
from aoc import AdventOfCode

# NOTE: Had to change algorithm to match part 2, in order to test
# Input Parse
puzzle = AdventOfCode(year=2019, day=22)
puzzle_input = puzzle.get_input()

def power_mod(a, x, m):
    # Finds value of (a ** x) % m recursively
    if x == 0:
        return 1
    p = power_mod(a, x // 2, m)
    res = (p ** 2 * (a * (x % 2) + (x + 1)%2)) % m
    # print(x, ">", res)
    return res

assert power_mod(7, 11, 101) == (7 ** 11) % 101

def mod_inverse(a, m):
    # Finds x such that (a*x) % m === 0 % m
    x = 1
    y = 0
    _a = a
    _m = m
    while _a > 1:
        # Basically euclid's formula
        q = _a // _m
        _a, _m = _m, _a % _m
        x, y = y, x - q*y
    assert (x % m) >= 0
    assert _a == 1, f"{_a}"
    return x % m

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

    def repeat_shuffle(self, shuffle_instructions, num_repeats):
            # result = f^M(i) where f(i) = (ai + b) % N
            #        = {i*a^M + b*sum_from_0_to_(M-1)[a^n]} %N
            #        = {i*a^M + b*(a^M - 1)/(a - 1)}%N
            #        = {i*a^M + b*(a^M - 1)/(a - 1)}%N
            # result = f^(M)(i) = (a^M * i + b(a^M - 1)/(a - 1)) % N
        self.shuffle(shuffle_instructions)
        self.add_coeff %= self.num_cards
        self.prod_coeff %= self.num_cards
        self.add_coeff *= power_mod(self.prod_coeff, num_repeats, self.num_cards) - 1
        # self.add_coeff %= self.num_cards
        self.add_coeff *= mod_inverse(self.prod_coeff - 1, self.num_cards)
        self.prod_coeff = power_mod(self.prod_coeff, num_repeats, self.num_cards)
        self.add_coeff %= self.num_cards
        self.prod_coeff %= self.num_cards

    def find_card(self, card_number):
        # Finds (a*i + b) % N
        return (self.add_coeff + self.prod_coeff*card_number) % self.num_cards

    def get_card_at(self, index):
        # Solves (a*i + b) === n (mod N)
        # ai + b === n (mod N)
        index -= self.add_coeff
        index %= self.num_cards
        
        # ai === n - b (mod N)
        index *= mod_inverse(self.prod_coeff, self.num_cards)
        # i === (n - b)/a (mod N)
        return index % self.num_cards

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.add_coeff, self.prod_coeff) == (other.add_coeff, other.prod_coeff)

# Actual Code 
deck = Deck(num_cards=119_315_717_514_047)
card_of_interest = 2020
deck.repeat_shuffle(puzzle_input, num_repeats=101_741_582_076_661)
card = deck.get_card_at(card_of_interest)
print(card)
# print(deck.find_card(card))