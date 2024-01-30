---
title: "Data Structures & Algorithms"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- What's the most efficient way to construct a list?
- When should Tuples be used?
- When should generator functions be used?
- When are sets appropriate?
- What is the best way to search a list?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Able to summarise how Lists and Tuples work behind the scenes.
- Able to identify appropriate use-cases for tuples.
- Able to use generator functions in appropriate situations.
- Able to utilise dictionaries and sets effectively
- Able to use `bisect_left()` to perform a binary search of a list or array

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


## Dictionaries

Dictionaries are another fundamental Python data-structure.
They provide a key-value store, whereby unique keys with no intrinsic order map to attached values.

::::::::::::::::::::::::::::::::::::: callout

> no intrinsic order

Since Python 3.6, the items within a dictionary will iterate in the order that they were inserted. This does not apply to sets.

`OrderedDict` still exists, and may be preferable if the order of items is important when performing whole-dictionary equality.

:::::::::::::::::::::::::::::::::::::::::::::

### Hashing Data Structures

<!-- simple explanation of how a hash-based data structure works -->
Python's dictionaries are implemented as hashing data structures.
Within a hashing data structure each inserted key is hashed to produce a (hopefully unique) integer key.
The dictionary is pre-allocated to a default size, and the key is assigned the index within the dictionary equivalent to the hash modulo the length of the dictionary.
If that index doesn't already contain another key, the key (and any associated values) can be inserted.
When the index isn't free, a collision strategy is applied. CPython's [dictionary](https://github.com/python/cpython/blob/main/Objects/dictobject.c) and [set](https://github.com/python/cpython/blob/main/Objects/setobject.c) both use a form of open addressing whereby a hash is mutated and corresponding indices probed until a free one is located.
When the hashing data structure exceeds a given load factor (e.g. 2/3 of indices have been assigned keys), the internal storage must grow. This process requires every item to be re-inserted which can be expensive, but reduces the average probes for a key to be found.

![An visual explanation of linear probing, CPython uses an advanced form of this.](episodes/fig/hash_linear_probing.png){alt='A diagram demonstrating how the keys (hashes) 37, 64, 14, 94, 67 are inserted into a hash table with 11 indices. This is followed by the insertion of 59, 80 and 39 which require linear probing to be inserted due to collisions.'}

To retrieve or check for the existence of a key within a hashing data structure, the key is hashed again and a process equivalent to insertion is repeated. However, now the key at each index is checked for equality with the one provided. If any empty index is found before an equivalent key, then the key must not be present in the ata structure.


### Keys

Keys will typically be a core Python type such as a number or string. However multiple of these can be combined as a Tuple to form a compound key, or a custom class can be used if the methods `__hash__()` and `__eq__()` have been implemented.

You can implement `__hash__()` by utilising the ability for Python to hash tuples, avoiding the need to implement a bespoke hash function.

```python
class MyKey:

    def __init__(self, _a, _b, _c):
        self.a = _a
        self.b = _b
        self.c = _c

    def __eq__(self, other):
        return (isinstance(other, type(self))
                and (self.a, self.b, self.c) == (other.a, other.b, other.c))

    def __hash__(self):
        return hash((self.a, self.b, self.c))

dict = {}
dict[MyKey("one", 2, 3.0)] = 12
```
The only limitation is that two objects where two objects are equal they must have the same hash, hence all member variables which contribute to `__eq__()` should also contribute to `__hash__()` and vice versa (it's fine to have irrelevant or redundant internal members contribute to neither).

## Sets

Sets are dictionaries without the values (both are declared using `{}`), a collection of unique keys equivalent to the mathematical set. *Modern CPython now uses a set implementation distinct from that of it's dictionary, however they still behave much the same in terms of performance characteristics.*

Sets are used for eliminating duplicates and checking for membership, and will normally outperform lists especially when the list cannot be maintained sorted.

::::::::::::::::::::::::::::::::::::: challenge

## Unique Collection

There are four implementations in the below example code, each builds a collection of unique elements from 25,000 where 50% can be expected to be duplicates.

Estimate how the performance of each approach is likely to stack up.

If you reduce the value of `repeats` it will run faster, how does changing the number of items (`N`) or the ratio of duplicates `int(N/2)` affect performance?

```python
import random
from timeit import timeit

def generateInputs(N = 25000):
    random.seed(12)  # Ensure every list is the same 
    return [random.randint(0,int(N/2)) for i in range(N)]
    
def uniqueSet():
    ls_in = generateInputs()
    set_out = set(ls_in)
    
def uniqueSetAdd():
    ls_in = generateInputs()
    set_out = set()
    for i in ls_in:
        set_out.add(i)
    
def uniqueList():
    ls_in = generateInputs()
    ls_out = []
    for i in ls_in:
        if not i in ls_out:
            ls_out.append(i)

def uniqueListSort():
    ls_in = generateInputs()
    ls_in.sort()
    ls_out = [ls_in[0]]
    for i in ls_in:
        if ls_out[-1] != i:
            ls_out.append(i)
            
repeats = 1000
gen_time = timeit(generateInputs, number=repeats)
print(f"uniqueSet: {timeit(uniqueSet, number=repeats)-gen_time:.2f}ms")
print(f"uniqueSetAdd: {timeit(uniqueSetAdd, number=repeats)-gen_time:.2f}ms")
print(f"uniqueList: {timeit(uniqueList, number=repeats)-gen_time:.2f}ms")
print(f"uniqueListSort: {timeit(uniqueListSort, number=repeats)-gen_time:.2f}ms")
```

:::::::::::::::::::::::: hint

* `uniqueSet()` passes the input list to the constructor `set()`.
* `uniqueSetAdd()` creates an empty set, and then iterates the input list adding each item individually.
* `uniqueList()` this naive approach, checks whether each item in the input list exists in the output list before appending.
* `uniqueListSort()` sorts the input list, allowing only the last item of the output list to be checked before appending.

*There is not a version using list comprehension, as it is not possible to refer to the list being constructed during list comprehension.*

:::::::::::::::::::::::::::::::::

:::::::::::::::::::::::: solution

Constructing a set by passing in a single list is the clear winner.

Constructing a set with a loop and `add()` (equivalent to a list's `append()`) comes in second. This is slower due to the pythonic loop, whereas adding a full list at once moves this to CPython's back-end.

The naive list approach is 2200x times slower than the fastest approach, because of how many times the list is searched. This gap will only grow as the number of items increases.

Sorting the input list reduces the cost of searching the output list significantly, however it is still 8x slower than the fastest approach. In part because around half of it's runtime is now spent sorting the list.

```output
uniqueSet: 0.30ms
uniqueSetAdd: 0.81ms
uniqueList: 660.71ms
uniqueListSort: 2.67ms
```
:::::::::::::::::::::::::::::::::
:::::::::::::::::::::::::::::::::::::::::::::::

## Searching

Independent of the performance to construct a unique set (as covered in the previous section), it's worth identifying the performance to search the data-structure to retrieve an item or check whether it exists.

The performance of a hashing data structure is subject to the load factor and number of collisions. An item that hashes with no collision can be checked almost directly, whereas one with collisions will probe until it finds the correct item or an empty slot. In the worst possible case, whereby all insert items have collided this would mean checking every single item. In practice, hashing data-structures are designed to minimise the chances of this happening and most items should be found or identified as missing with a single access.

In contrast if searching a list or array, the default approach is to start at the first item and check all subsequent items until the correct item has been found. If the correct item is not present, this will require the entire list to be checked. Therefore the worst-case is similar to that of the hashing data-structure, however it is guaranteed in cases where the item is missing. Similarly, on-average we would expect an item to be found half way through the list, meaning that an average search will require checking half of the items.

If however the list or array is sorted, a binary search can be used. A binary search divides the list in half and checks which half the target item would be found in, this continues recursively until the search is exhausted whereby the item should be found or dismissed. This is significantly faster than performing a linear search of the list, checking a total of `log N` items every time.

The below code demonstrates these approaches and their performance.

```python
import random
from timeit import timeit
from bisect import bisect_left

N = 25000  # Number of elements in list
M = 2  # N*M == Range over which the elements span

def generateInputs():
    random.seed(12)  # Ensure every list is the same
    st = set([random.randint(0, int(N*M)) for i in range(N)])
    ls = list(st)
    ls.sort()  # Sort required for binary
    return st, ls  # Return both set and list
    
def search_set():
    st, _ = generateInputs()
    j = 0
    for i in range(0, int(N*M), M):
        if i in st:
            j += 1
    
def linear_search_list():
    _, ls = generateInputs()
    j = 0
    for i in range(0, int(N*M), M):
        if i in ls:
            j += 1
    
def binary_search_list():
    _, ls = generateInputs()
    j = 0
    for i in range(0, int(N*M), M):
        k = bisect_left(ls, i)
        if k != len(ls) and ls[k] == i:
            j += 1

            
repeats = 1000
gen_time = timeit(generateInputs, number=repeats)
print(f"search_set: {timeit(search_set, number=repeats)-gen_time:.2f}ms")
print(f"linear_search_list: {timeit(linear_search_list, number=repeats)-gen_time:.2f}ms")
print(f"binary_search_list: {timeit(binary_search_list, number=repeats)-gen_time:.2f}ms")
```

Searching the set is fastest performing 25,000 searches in 0.04ms.
This is  followed by the binary search of the (sorted) list which is 145x slower, although the list has been filtered for duplicates. A list still containing duplicates would be longer, leading to a more expensive search.
The linear search of the list is more than 56,600x slower than the fastest, it really shouldn't be used!

```output
search_set: 0.04ms
linear_search_list: 2264.91ms
binary_search_list: 5.79ms
```

These results are subject to change based on the number of items and the proportion of searched items that exist within the list. However, the pattern is likely to remain the same. Linear searches should be avoided!


::::::::::::::::::::::::::::::::::::: keypoints

- List comprehension should be preferred when constructing lists.
- Where appropriate, Tuples and Generator functions should be preferred over Python lists.
- Dictionaries and sets are appropriate for storing a collection of unique data with no intrinsic order for random access.
- When used appropriately, dictionaries and sets are significantly faster than lists.
- If searching a list or array is required, it should be sorted and searched using `bisect_left()` (binary search).

::::::::::::::::::::::::::::::::::::::::::::::::
