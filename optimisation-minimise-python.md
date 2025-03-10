---
title: "Understanding Python (NumPy/Pandas)"
teaching: 30
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- Why is NumPy often faster than raw Python?
- How can processing rows of a Pandas data table be made faster?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Able to utilise NumPy's vectorisation when operating on arrays of data.
- Able to efficiently process rows when working with data tables.

::::::::::::::::::::::::::::::::::::::::::::::::

Earlier, we saw that builtin functions in Python, like `sum()`, are often faster than manually looping over a list. This is because those high-level functions are able to do most of the work in the C backend

Packages like NumPy and Pandas work similarly: They have been written in compiled languages to expose this performance across a wide range of scientific workloads.



## Using NumPy (Effectively)

[NumPy](https://numpy.org/) is a commonly used package for scientific computing, which provides a wide variety of methods.

It adds restriction via it's own [basic numeric types](https://numpy.org/doc/stable/user/basics.types.html), and static arrays to enable even greater performance than that of core Python. However if these restrictions are ignored, the performance can become significantly worse.

### Arrays

NumPy's arrays (not to be confused with the core Python `array` package) are static arrays. Unlike core Python's lists, they do not dynamically resize. Therefore if you wish to append to a NumPy array, you must call `resize()` first. If you treat this like `append()` for a Python list, resizing for each individual append you will be performing significantly more copies and memory allocations than a Python list.

The below example sees lists and arrays constructed from `range(100000)`.

```python
from timeit import timeit
import numpy

N = 100000  # Number of elements in list/array

def list_append():
    ls = []
    for i in range(N):
        ls.append(i)

def array_resize():
    ar = numpy.zeros(1)
    for i in range(1, N):
        ar.resize(i+1)
        ar[i] = i
        
repeats = 1000
print(f"list_append: {timeit(list_append, number=repeats):.2f}ms")
print(f"array_resize: {timeit(array_resize, number=repeats):.2f}ms")
```

Resizing a NumPy array is 5.2x slower than a list, probably 10x slower than list comprehension.

```output
list_append: 3.50ms
array_resize: 18.04ms
```

Another difference, is that NumPy arrays typically require all data to be the same type (and a NumPy type). This enables more efficient access to elements, as they all exist contiguously in memory. In contrast, elements within Python lists can be of any type so the list always stores a pointer to where the element actually exists in memory, rather than the actual element. This has the side effect that if you are converting back and forth between Python lists and NumPy arrays, there is an additional overhead as it's not as simple as copying a single block of memory.

::::::::::::::::::::::::::::::::::::: callout

If you construct a NumPy array from a list containing a complex object, it will store your data as Python types and you won't be able to take advantage of NumPy's optimisations.

```sh
>python
>>> import numpy as np
>>> a = np.array([0.5, 5])
>>> type(a[0])
<class 'numpy.float64'>
>>> type(a[1])
<class 'numpy.float64'>
>>> b = np.array([0.5, 5,{"foo":5}])
>>> type(b[0])
<class 'float'>
>>> type(b[1])
<class 'int'>
>>> type(b[2])
<class 'dict'>
```

:::::::::::::::::::::::::::::::::::::::::::::

The below example demonstrates the overhead of mixing Python lists and NumPy functions.

```sh
# Python list, numpy.random.choice()
>python -m timeit -s "import numpy; ls = list(range(10000))" "numpy.random.choice(ls)"
1000 loops, best of 5: 267 usec per loop

# NumPy array, numpy.random.choice()
>python -m timeit -s "import numpy; ar = numpy.arange(10000)" "numpy.random.choice(ar)"
50000 loops, best of 5: 4.06 usec per loop
```

Passing a Python list to `numpy.random.choice()` is 65.6x slower than passing a NumPy array. This is the additional overhead of converting the list to an array. If this function were called multiple times, it would make sense to transform the list to an array before calling the function so that overhead is only paid once.

::::::::::::::::::::::::::::::::::::: callout

```sh
# Python list, Manually select 1 item
>python -m timeit -s "import numpy; ls = list(range(10000))" "ls[numpy.random.randint(len(ls))]"
200000 loops, best of 5: 1.19 usec per loop

# NumPy array, Manually select 1 item
>python -m timeit -s "import numpy; ar = numpy.arange(10000)" "ar[numpy.random.randint(len(ar))]"
200000 loops, best of 5: 1.22 usec per loop
```

Regardless, for this simple application of `numpy.random.choice()`, merely using `numpy.random.randint(len())` is around 4x faster regardless whether a Python list or NumPy array is used. 

With `numpy.random.choice()` being such a general function (it has many possible parameters), there is significant internal branching. If you don't require this advanced functionality and are calling a function regularly, it can be worthwhile considering using a more limited function.

There is however a trade-off, using `numpy.random.choice()` can be clearer to someone reading your code, and is more difficult to use incorrectly.

:::::::::::::::::::::::::::::::::::::::::::::

### Vectorisation

The manner by which NumPy stores data in arrays enables it's functions to utilise vectorisation, whereby the processor executes one instruction across multiple variables simultaneously, for every mathematical operation between arrays.

Earlier in this episode it was demonstrated that using core Python methods over a list, will outperform a loop performing the same calculation faster. The below example takes this a step further by demonstrating the calculation of dot product.

<!-- Inspired by High Performance Python Chapter 6 example 
Added python sum array, skipped a couple of others--> 
```python
from timeit import timeit

N = 1000000  # Number of elements in list

gen_list = f"ls = list(range({N}))"
gen_array = f"import numpy;ar = numpy.arange({N}, dtype=numpy.int64)"

py_sum_ls = "sum([i*i for i in ls])"
py_sum_ar = "sum(ar*ar)"
np_sum_ar = "numpy.sum(ar*ar)"
np_dot_ar = "numpy.dot(ar, ar)"

repeats = 1000
print(f"python_sum_list: {timeit(py_sum_ls, setup=gen_list, number=repeats):.2f}ms")
print(f"python_sum_array: {timeit(py_sum_ar, setup=gen_array, number=repeats):.2f}ms")
print(f"numpy_sum_array: {timeit(np_sum_ar, setup=gen_array, number=repeats):.2f}ms")
print(f"numpy_dot_array: {timeit(np_dot_ar, setup=gen_array, number=repeats):.2f}ms")
```

* `python_sum_list` uses list comprehension to perform the multiplication, followed by the Python core `sum()`. This comes out at 46.93ms
* `python_sum_array` instead directly multiplies the two arrays, taking advantage of NumPy's vectorisation. But uses the core Python `sum()`, this comes in slightly faster at 33.26ms.
* `numpy_sum_array` again takes advantage of NumPy's vectorisation for the multiplication, and additionally uses NumPy's `sum()` implementation. These two rounds of vectorisation provide a much faster 1.44ms completion.
* `numpy_dot_array` instead uses NumPy's `dot()` to calculate the dot product in a single operation. This comes out the fastest at 0.29ms, 162x faster than `python_sum_list`. 

```output
python_sum_list: 46.93ms
python_sum_array: 33.26ms
numpy_sum_array: 1.44ms
numpy_dot_array: 0.29ms
```

::::::::::::::::::::::::::::::::::::: callout

## Parallel NumPy

<!-- https://superfastpython.com/multithreaded-numpy-functions/ -->
NumPy can sometimes take advantage of auto parallelisation, particularly on HPC systems.

A small number of functions are backed by BLAS and LAPACK, enabling even greater speedup.

The [supported functions](https://numpy.org/doc/stable/reference/routines.linalg.html) mostly correspond to linear algebra operations.

The auto-parallelisation of these functions is hardware dependant, so you won't always automatically get the additional benefit of parallelisation.
However, HPC systems should be primed to take advantage, so try increasing the number of cores you request when submitting your jobs and see if it improves the performance.

*This might be why `numpy_dot_array` is that much faster than `numpy_sum_array` in the previous example!*

:::::::::::::::::::::::::::::::::::::

### `vectorize()`

Python's `map()` was introduced earlier, for applying a function to all elements within a list.
NumPy provides `vectorize()` an equivalent for operating over it's arrays.

This doesn't actually make use of processor-level vectorisation, from the [documentation](https://numpy.org/doc/stable/reference/generated/numpy.vectorize.html):

> The `vectorize` function is provided primarily for convenience, not for performance. The implementation is essentially a for loop.

The below example demonstrates how the performance of `vectorize()` is only marginally faster than `map()`.

```python
N = 100000  # Number of elements in list/array

def genArray():
    return numpy.arange(N)

def plus_one(x):
    return x + 1
    
def python_map():
    ar = genArray()
    return list(map(plus_one, ar))

def numpy_vectorize():
    ar = genArray()
    return numpy.vectorize(plus_one)(ar)

repeats = 1000
gentime = timeit(genArray, number=repeats)
print(f"python_map: {timeit(python_map, number=repeats)-gentime:.2f}ms")
print(f"numpy_vectorize: {timeit(numpy_vectorize, number=repeats)-gentime:.2f}ms")
```

```output
python_map: 7.94ms
numpy_vectorize: 7.80ms
```

## Using Pandas (Effectively)

[Pandas](https://pandas.pydata.org/) is the most common Python package used for scientific computing when working with tabular data akin to spreadsheets (DataFrames).

Similar to NumPy, Pandas enables greater performance than pure Python implementations when used correctly, however incorrect usage can actively harm performance.

## Operating on Rows

Pandas' methods by default operate on columns. Each column or series can be thought of as a NumPy array, highly suitable for vectorisation.

Following the theme of this episode, iterating over the rows of a data frame using a `for` loop is not advised. The pythonic iteration will be slower than other approaches.

Pandas allows it's own methods to be applied to rows in many cases by passing `axis=1`, where available these functions should be preferred over manual loops. Where you can't find a suitable method, `apply()` can be used, which is similar to `map()`/`vectorize()`, to apply your own function to rows.

```python
from timeit import timeit
import pandas
import numpy

N = 100000  # Number of rows in DataFrame

def genDataFrame():
    numpy.random.seed(12)  # Ensure each dataframe is identical
    return pandas.DataFrame(
    {
        "f_vertical": numpy.random.random(size=N),
        "f_horizontal": numpy.random.random(size=N),
        # todo some spurious columns
    })

def pythagoras(row):
    return (row["f_vertical"]**2 + row["f_horizontal"]**2)**0.5
    
def for_range():
    rtn = []
    df = genDataFrame()
    for row_idx in range(df.shape[0]):
        row = df.iloc[row_idx]
        rtn.append(pythagoras(row))
    return pandas.Series(rtn)

def for_iterrows():
    rtn = []
    df = genDataFrame()
    for row_idx, row in df.iterrows():
        rtn.append(pythagoras(row))
    return pandas.Series(rtn)
    
def pandas_apply():
    df = genDataFrame()
    return df.apply(pythagoras, axis=1)

repeats = 100
gentime = timeit(genDataFrame, number=repeats)
print(f"for_range: {timeit(for_range, number=repeats)*10-gentime:.2f}ms")
print(f"for_iterrows: {timeit(for_iterrows, number=repeats)*10-gentime:.2f}ms")
print(f"pandas_apply: {timeit(pandas_apply, number=repeats)*10-gentime:.2f}ms")
```

`apply()` is 3x faster than the two `for` approaches, as it avoids the Python `for` loop.


```output
for_range: 1582.47ms
for_iterrows: 1677.14ms
pandas_apply: 390.49ms
```

However, rows don't exist in memory as arrays (columns do!), so `apply()` does not take advantage of NumPys vectorisation. You may be able to go a step further and avoid explicitly operating on rows entirely by passing only the required columns to NumPy.

```python
def vectorize():
    df = genDataFrame()
    return pandas.Series(numpy.sqrt(numpy.square(df["f_vertical"]) + numpy.square(df["f_horizontal"])))
    
print(f"vectorize: {timeit(vectorize, number=repeats)-gentime:.2f}ms")
```

264x faster than `apply()`, 1000x faster than `for` `iterrows()`!

```
vectorize: 1.48ms
```

It won't always be possible to take full advantage of vectorisation, for example you may have conditional logic.

An alternate approach is converting your dataframe to a Python dictionary using `to_dict(orient='index')`. This creates a nested dictionary, where each row of the outer dictionary is an internal dictionary. This can then be processed via list-comprehension:

```python
def to_dict():
    df = genDataFrame()
    df_as_dict = df.to_dict(orient='index')
    return pandas.Series([(r['f_vertical']**2 + r['f_horizontal']**2)**0.5 for r in df_as_dict.values()])

print(f"to_dict: {timeit(to_dict, number=repeats)*10-gentime:.2f}ms")
```

Whilst still nearly 100x slower than pure vectorisation, it's twice as fast as `apply()`.

```sh
to_dict: 131.15ms
```

This is because indexing into Pandas' `Series` (rows) is significantly slower than a Python dictionary. There is a slight overhead to creating the dictionary (40ms in this example), however the stark difference in access speed is more than enough to overcome that cost for any large dataframe.

```python
from timeit import timeit
import pandas as pandas

N = 100000  # Number of rows in DataFrame

def genInput():
    s = pandas.Series({'a' : 1, 'b' : 2})
    d = {'a' : 1, 'b' : 2}
    return s, d

def series():
    s, _ = genInput()
    for i in range(N):
        y = s['a'] * s['b']

def dictionary():
    _, d = genInput()
    for i in range(N):
        y = d['a'] * d['b']

repeats = 1000
print(f"series: {timeit(series, number=repeats):.2f}ms")
print(f"dictionary: {timeit(dictionary, number=repeats):.2f}ms")
```

65x slower!

```output
series: 237.25ms
dictionary: 3.63ms
```

## Filter Early

If you can filter your rows before processing, rather than after, you may significantly reduce the amount of processing and memory used.

::::::::::::::::::::::::::::::::::::: keypoints

- Python is an interpreted language, this adds an additional overhead at runtime to the execution of Python code. Many core Python and NumPy functions are implemented in faster C/C++, free from this overhead.
- NumPy can take advantage of vectorisation to process arrays, which can greatly improve performance.
- Pandas' data tables store columns as arrays, therefore operations applied to columns can take advantage of NumPys vectorisation.

::::::::::::::::::::::::::::::::::::::::::::::::
