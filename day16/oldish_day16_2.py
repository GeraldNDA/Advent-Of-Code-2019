#!/usr/bin/env python3
# Imports
import numpy
from collections import defaultdict

from aoc import AdventOfCode

# Input Parse
puzzle = AdventOfCode(year=2019, day=16)
puzzle_input = puzzle.get_input()
puzzle_input = tuple(map(int, puzzle_input))

SIGNAL = puzzle_input
SIGNAL_SIZE = len(SIGNAL)
SIGNAL_REPEAT = 10000

FFT_RESULT = {}
def lazy_fft(idx, phase):
    while (idx, phase) not in FFT_RESULT:
        if phase == 0:
            FFT_RESULT[idx, phase] = SIGNAL[idx % SIGNAL_SIZE]
            break

        res = 0
        amount = idx + 1
        start_idx = idx
        multiplier = 1
        while start_idx < SIGNAL_SIZE*SIGNAL_REPEAT:
            end_idx = start_idx + amount
            end_idx = min(end_idx, SIGNAL_SIZE*SIGNAL_REPEAT)
            if start_idx == idx and (start_idx - 1, phase) in FFT_RESULT and 2*start_idx - 1 >= SIGNAL_SIZE*SIGNAL_REPEAT:
                res = FFT_RESULT[start_idx - 1, phase] + 10 - FFT_RESULT[start_idx - 1, phase - 1]
            else:
                res += multiplier*sum(lazy_fft(fft_idx, phase - 1) for fft_idx in range(start_idx, end_idx))

            multiplier *= -1
            start_idx += 2*amount

        if res < 0:
            res *= -1

        FFT_RESULT[idx, phase] = res % 10

    return FFT_RESULT[idx, phase]

message_offset = int("".join(map(str, SIGNAL[:7])))
phase_count = 100
res = ""
for fft_idx in range(message_offset, message_offset+8):
    res += str(lazy_fft(fft_idx, phase_count))
print(res)