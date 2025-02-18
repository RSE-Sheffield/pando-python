import random
from timeit import timeit

N = 10_000  # Number of elements in the list

# Ensure every list is the same
random.seed(12)
f = [f" {i:0>6d} {random.random():8.4f} " for i in range(N)]

def manualSplit():  # bad habits
    data = {}
    for line in f:
        first_char = line.find("0")
        end_time = line.find(" ", first_char, -1)

        energy_found = line.find(".", end_time, -1)
        begin_energy = line.rfind(" ", end_time, energy_found)
        end_energy = line.find(" ", energy_found, -1)
        if end_energy == -1:
            end_energy = len(line)
        
        time = line[first_char:end_time]
        energy = line[begin_energy:end_energy]

        data[time] = energy
    return data

def builtinSplit():
    data = {}
    for line in f:
        time, energy = line.split()
        data[time] = energy
    return data

def dictComprehension():
    return {time: energy for time, energy in (line.split() for line in f)}


repeats = 1000
print(f"manualSplit: {timeit(manualSplit, globals=globals(), number=repeats):.3f}ms")
print(f"builtinSplit: {timeit(builtinSplit, globals=globals(), number=repeats):.3f}ms")
print(f"dictComprehension: {timeit(dictComprehension, globals=globals(), number=repeats):.3f}ms")
