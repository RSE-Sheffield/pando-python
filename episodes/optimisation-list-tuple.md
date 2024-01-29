---
title: "Lists (& Tuples)"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- What's the most efficient way to construct a list?
- When should Tuples be used?
- When should generator functions be used?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Able to summarise how Lists and Tuples work behind the scenes.
- Able to identify appropriate use-cases for tuples.
- Able to use generator functions in appropriate situations.

::::::::::::::::::::::::::::::::::::::::::::::::

## Lists

Lists are a fundamental data structure within Python.

It is implemented as a form of dynamic array found within many programming languages by different names (C++: `std::vector`, Java: `ArrayList`, R: `vector`, Julia: `Vector`).

They allows direct and sequential element access, with the convenience to append items.

This is achieved by internally storing items in a static array.
This array however can be longer than the `List`.
When an item is added, the `List` checks whether it has enough spare space to add the item to the end.
If it doesn't, it will reallocate a larger array, copy across the elements, and deallocate the old array.

The growth is dependent on the implementation's growth factor.
CPython for example uses [`newsize + (newsize >> 3) + 6`](https://github.com/python/cpython/blob/a571a2fd3fdaeafdfd71f3d80ed5a3b22b63d0f7/Objects/listobject.c#L74), which works out to an over allocation of roughly ~12.5%.

![The relationship between the number of appends to an empty list, and the number of internal resizes in CPython.](episodes/fig/cpython_list_allocations.png){alt='A line graph displaying the relationship between the number of calls to append() and the number of internal resizes of a CPython list. It has a logarithmic relationship, at 1 million appends there have been 84 internal resizes.'}

This has two implications:

* If you are creating large static lists, they will use upto 12.5% excess memory.
* If you are growing a list with `append()`, there will be large amounts of redundant allocations and copies as the list grows.

### List Comprehension

If creating a list via `append()` is undesirable, the natural alternative is to use list-comprehension.

List comprehension can be twice as fast at building lists than using `append()`.
This is primarily because list-comprehension allows Python to offload much of the computation into faster C code.
General python loops in contrast can be used for much more, so they remain in Python bytecode during computation which has additional overheads.

This can be demonstrated with the below benchmark:

```python
from timeit import timeit

def list_append():
    li = []
    for i in range(100000):
        li.append(i)

def list_preallocate():
    li = [0]*100000
    for i in range(100000):
        li[i] = i

def list_comprehension():
    li = [i for i in range(100000)]

repeats = 1000
print(f"Append: {timeit(list_append, number=repeats):.2f}ms")
print(f"Preallocate: {timeit(list_preallocate, number=repeats):.2f}ms")
print(f"Comprehension: {timeit(list_comprehension, number=repeats):.2f}ms")
```

`timeit` is used to run each function 1000 times, providing the below averages:

```output
Append: 3.50ms
Preallocate: 2.48ms
Comprehension: 1.69ms
```

Results will vary between Python versions, hardware and list lengths. But in this example list comprehension was 2x faster, with pre-allocate fairing in the middle. Although this is milliseconds, this can soon add up if you are regularly creating lists.

## Tuples

In contrast, Python's Tuples are immutable static arrays (similar to strings), their elements cannot be modified and they cannot be resized.

Their potential use-cases are greatly reduced due to these two limitations, they are only suitable for groups of immutable properties.

Tuples can still be joined with the `+` operator, similar to appending lists, however the result is always a newly allocated tuple (without a list's over-allocation).

Python caches a large number of short (1-20 element) tuples. This greatly reduces the cost of creating and destroying them during execution at the cost of a slight memory overhead.

This can be easily demonstrated with Python's `timeit` module in your console.

```sh
>python -m timeit "li = [0,1,2,3,4,5]"
10000000 loops, best of 5: 26.4 nsec per loop

>python -m timeit "tu = (0,1,2,3,4,5)"
50000000 loops, best of 5: 7.99 nsec per loop
```

It takes 3x as long to allocate a short list than a tuple of equal length. This gap only grows with the length, as the tuple cost remains roughly static whereas the cost of allocating the list grows slightly.


## Generator Functions

You may not even require your data be stored in a list or tuple if it is only accessed once and in sequence.

Generators are special functions, that use `yield` rather than `return`. Each time the generator is called, it resumes computation until the next `yield` statement is hit to return the next value.

This avoids needing to allocate a data structure, and can greatly reduce memory utilisation.

Common examples for generators include:
* Reading from a large file that may not fit in memory.
* Any generated sequence where the required length is unknown.

The below example demonstrates how a generator function (`fibonnaci_generator()`) differs from one that simply returns a constructed list (`fibonacci_list()`).

```python
from timeit import timeit

N = 1000000
repeats = 1000

def fibonacci_generator():
    a=0
    b=1
    while True:
        yield b
        a,b= b,a+b
        
def fibonacci_list(max_val):
    rtn = []
    a=0
    b=1
    while b < max_val:
        rtn.append(b)
        a,b= b,a+b
    return rtn

def test_generator():
    t = 0
    max_val = N
    for i in fibonacci_generator():
        if i > max_val:
            break
        t += i

def test_list():
    li = fibonacci_list(N)
    t = 0
    for i in li:
        t += i
        
def test_list_long():
    t = 0
    max_val = N
    li = fibonacci_list(max_val*10)
    for i in li:
        if i > max_val:
            break
        t += i

print(f"Gen: {timeit(test_generator, number=repeats):.5f}ms")
print(f"List: {timeit(test_list, number=repeats):.5f}ms")
print(f"List_long: {timeit(test_list_long, number=repeats):.5f}ms")
```

The performance of `test_generator()` and `test_list()` are comparable, however `test_long_list()` which generates a list with 5 extra elements (35 vs 30) is consistently slower.

```output
Gen: 0.00251ms
List: 0.00256ms
List_long: 0.00332ms
```

Unlike list comprehension, a generator function will normally involve a Python loop. Therefore, their performance is typically slower than constructing a list where much of the computation can be offloaded to the CPython backend.

::::::::::::::::::::::::::::::::::::: callout

The use of `max_val` in the previous example moves the value of `N` from global to local scope.

The Python interpreter checks local scope first when finding variables, therefore this makes accessing local scope variables slightly faster than global scope, this is most visible when a variable is being accessed regularly such as within a loop.

Replacing the use of `max_val` with `N` inside `test_generator()` causes the function to consistently perform a little slower than `test_list()`, whereas before the change it would normally be a little faster.

:::::::::::::::::::::::::::::::::::::::::::::



::::::::::::::::::::::::::::::::::::: keypoints

- List comprehension should be preferred when constructing lists.
- Where appropriate, Tuples and Generator functions should be preferred over Python lists.

::::::::::::::::::::::::::::::::::::::::::::::::
