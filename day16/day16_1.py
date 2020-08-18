#!/usr/bin/env python3
# Imports
from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=16)
puzzle_input = puzzle.get_input()
# puzzle_input = "12345678"

signal = [int(d) for d in puzzle_input]

def apply_fft_single(signal, pattern):
    assert len(pattern) == len(signal)
    return [signal_el*pattern_el  for pattern_el, signal_el in zip(signal, pattern)]


def get_pattern(idx, pattern_len):
    idx += 1
    initial_pattern =  [0]*idx + [1]*idx +[0]*idx + [-1]*idx
    pattern = initial_pattern * ((pattern_len+1) // len(initial_pattern))
    return (pattern + initial_pattern[0:(pattern_len + 1 - len(pattern))])[1:]

def apply_fft(signal):
    pattern_len = len(signal)
    res =  [sum(apply_fft_single(signal, get_pattern(idx, pattern_len))) for idx, digit in enumerate(signal)]
    return [int(str(num)[-1]) for num in res]
# Actual Code
for _ in range(100):
    print(_)
    signal = apply_fft(signal)


# Result
# print(signal)
print("".join(map(str, signal[:8])))