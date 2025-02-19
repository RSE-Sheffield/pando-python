from timeit import timeit
import numpy

N = 100_000  # Number of elements in list/array

def list_append():
    ls = []
    for i in range(N):
        ls.append(i)

def array_resize():
    ar = numpy.zeros(1)
    for i in range(1, N):
        ar.resize(i+1)
        ar[i] = i

def array_preallocate():
    ar = numpy.zeros(N)
    for i in range(1, N):
        ar[i] = i

repeats = 1000
print(f"list_append: {timeit(list_append, number=repeats):.2f}ms")
print(f"array_resize: {timeit(array_resize, number=repeats):.2f}ms")
print(f"array_preallocate: {timeit(array_preallocate, number=repeats):.2f}ms")
