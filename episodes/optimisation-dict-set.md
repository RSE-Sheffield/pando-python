---
title: "Lists & Sets"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- 

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- 

::::::::::::::::::::::::::::::::::::::::::::::::

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

## Checking Existence

<!-- Exercise to demonstrate performance of access vs list/numpy array-->

::::::::::::::::::::::::::::::::::::: keypoints

- Dictionaries and Sets are appropriate for storing a collection of unique data with no intrinsic order for random access
- When used appropriately, dictionaries and sets are significantly faster than lists.

::::::::::::::::::::::::::::::::::::::::::::::::
