---
title: "Using Python Language Features and the Standard Library"
teaching: 10
exercises: 5
---

:::::::::::::::::::::::::::::::::::::: questions

- TODO

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Able to utilise Python language features effectively
- Able to search Python documentation for functionality available in built-in types and in the standard library

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: instructor

This episode discusses relatively fundamental features of Python.

For students experienced with writing Python, many of these points may be unnecessary. However, self-taught students—especially if they have previously studied lower-level languages with a less powerful standard library—may have adopted “unpythonic” habits and will particularly benefit from this section.

::::::::::::::::::::::::::::::::::::::::::::::::

Before we look at data structures, algorithms and third-party libraries, we should take a few minutes to make sure we’re familiar with the fundamentals of Python.
If you’ve learned to program in another language, chances are you’ve picked up some habits from that language that don’t work well in Python.

Most of the bad habits that took me a while to unlearn—and that I’ve observed in others, too—come from learning to program in a lower-level language (like C or Delphi), with a less powerful standard library.


## Built-in Functions

For example, back when I was in undergrad, if you’d asked me to sum up a bunch of data points, I would have written something like the first function in this code sample:

```Python
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
```

Even just replacing the C-style iteration over indices with a more pythonic iteration over the elements themselves speeds up the code by about 2×.
But even better, by switching to the builtin `sum` function our code becomes about 8× faster, doing the exact same operation!

```output
manualSumC: 1.624ms
manualSumPy: 0.740ms
builtinSum: 0.218ms
```

This is because [built-in functions](https://docs.python.org/3/library/functions.html) (i.e. those that are available without importing packages) are typically implemented in the CPython back-end, so their performance benefits from bypassing the Python interpreter.

In particular, those which are passed an `iterable` (e.g. lists) are likely to provide the greatest benefits to performance. The Python documentation provides equivalent Python code for many of these cases.

* [`all()`](https://docs.python.org/3/library/functions.html#all): boolean and of all items
* [`any()`](https://docs.python.org/3/library/functions.html#all): boolean or of all items
* [`max()`](https://docs.python.org/3/library/functions.html#max): Return the maximum item 
* [`min()`](https://docs.python.org/3/library/functions.html#min): Return the minimum item 
* [`sum()`](https://docs.python.org/3/library/functions.html#sum): Return the sum of all items

<!-- todo exercise/s where pure-python must be converted to use one of the above fns. -->

This is a nice illustration of the principle we discussed earlier:
It is often best to tell the interpreter/library at a high level *what you want*, and let it figure out *how to do it*.


## Example: Parsing data from a text file

In C, since there is no high-level `string` datatype, parsing strings can be fairly arduous work where you repeatedly look for the index of a separator character in the string and use that index to split the string up.


::::::::::::::::::::::::::::::::::::: challenge

Let’s say we have read in some data from a text file, each line containing a time bin and a mean energy:

```python
f = [
    '   0   0.9819 ',
    '   1   0.3435 ',
    # ...
    '  99   0.2275 ',
    ' 100   0.7067 ',
    # ...
]
```

A colleague who learned programming in C wrote the following code to parse the data into a dictionary:
```python
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
        energy = line[begin_energy + 1:end_energy]

        data[time] = energy
    return data
```

Can you find a shorter, more easily understandable way to write this in Python?

<!-- Did you spot the bug in the manual implementation? ;) -->

:::::::::::::::::::::::: hint

Python strings have a lot of methods to perform common operations, like removing suffixes, replacing substrings, joining or splitting, stripping whitespaces, and much more. See the documentation at https://docs.python.org/3/library/stdtypes.html#string-methods for a full list.

:::::::::::::::::::::::::::::::::

:::::::::::::::::::::::: solution

```python

def builtinSplit():
    data = {}
    for line in f:
        time, energy = line.split()
        data[time] = energy
    return data
```

This is much more readable.
The code that’s executed by CPython may use similar indexing steps as in `manualSplit`; however, since this is all happening “under the hood” in C code, it is once again faster. 

```python

N = 10_000  # Number of elements in the list

# Ensure every list is the same
random.seed(12)
f = [f" {i:0>6d} {random.random():8.4f} " for i in range(N)]

repeats = 1000
print(f"manualSplit: {timeit(manualSplit, globals=globals(), number=repeats):.3f}ms")
print(f"builtinSplit: {timeit(builtinSplit, globals=globals(), number=repeats):.3f}ms")
```

```output
manualSplit: 1.797ms
builtinSplit: 0.796ms
```

:::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: challenge

If you’ve brought a project you want to work on: Do you have any similar code in there, which is hard to understand because it contains a lot of low-level step-by-step instructions?

:::::::::::::::::::::::: hint

Typical cases might include reading data from a file, …, … TODO: more examples?

:::::::::::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::