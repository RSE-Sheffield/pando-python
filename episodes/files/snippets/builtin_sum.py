import random
from timeit import timeit

N = 100_000  # Number of elements in the list

# Ensure every list is the same
random.seed(12)
my_data = [random.random() for i in range(N)]


def manualSumC():  # bad habits
    n = 0
    for i in range(len(my_data)):
        n += my_data[i]
    return n

def manualSumPy():  # slightly improved
    n = 0
    for evt_count in my_data:
        n += evt_count
    return n

def builtinSum():  # fastest and most readable
    return sum(my_data)


repeats = 1000
print(f"manualSumC: {timeit(manualSumC, globals=globals(), number=repeats):.3f}ms")
print(f"manualSumPy: {timeit(manualSumPy, globals=globals(), number=repeats):.3f}ms")
print(f"builtinSum: {timeit(builtinSum, globals=globals(), number=repeats):.3f}ms")
