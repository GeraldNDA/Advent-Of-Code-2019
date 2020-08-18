#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=4)
puzzle_input = puzzle.get_input()

# Actual Code
def valid_password(password):
    digits = str(password)
    if len(digits) != 6:
        return False
    if list(digits) != list(sorted(digits)):
        return False
    for n in set(digits):
        if digits.count(n) == 2:
            return True
    return False         
lower_bound, upper_bound = [int(n) for n in puzzle_input.split("-")]
valid_count = 0
for n in range(lower_bound, upper_bound+1):
    if valid_password(n):
        valid_count += 1
        print(n)
    
# for test in (112233, 123444, 111122):
#     print(test, valid_password(test))
    


# Result
print(valid_count)