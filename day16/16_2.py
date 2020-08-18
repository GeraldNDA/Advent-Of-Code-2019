puzzle_input *= 10000
print(len(puzzle_input))
# puzzle_input = "12345678"

signal = [int(d) for d in puzzle_input]
offset = int(puzzle_input[:7])

def apply_fft_single(signal, pattern):
    assert len(pattern) == len(signal)
    return [signal_el*pattern_el  for pattern_el, signal_el in zip(signal, pattern)]

PATTERN_CACHE = {}
def get_pattern(idx, pattern_len):
    if (idx, pattern_len) not in PATTERN_CACHE:
        idx += 1
        initial_pattern =  [0]*idx + [1]*idx +[0]*idx + [-1]*idx
        pattern = initial_pattern * ((pattern_len+1) // len(initial_pattern))
        return (pattern + initial_pattern[0:(pattern_len + 1 - len(pattern))])[1:]
    else:
        return PATTERN_CACHE[(idx, pattern_len)]
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
print("".join(map(str, signal[offset:offset+8])))