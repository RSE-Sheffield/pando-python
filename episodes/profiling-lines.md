---
title: "Line Level Profiling"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- When is line level profiling appropriate?
- What adjustments are required to Python code to profile with `line_profiler`?
- How can `line_profiler` be used to profile a Python program?
<!-- Last two overlap somewhat -->
::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- decorate Python code to prepare it for profiling with `line_profiler`
- execute a Python program via `line_profiler` to collect profiling information about a Python program’s execution
- interpret output from `line_profiler`, to identify the lines where time is being spent during a program’s execution

::::::::::::::::::::::::::::::::::::::::::::::::

## Introduction

<!-- Context -->
Whilst profiling, you may find that function-level profiling highlights expensive methods where you can't easily determine the cause of the cost due to their complexity.

<!-- What -->
Line level profiling allows you to target specific methods to collect more granular metrics, which can help narrow the source of expensive computation further. Typically line-level profiling will calculate the number of times each line is called and the total time spent executing each line. However, with the increased granularity come increased collection costs, which is why it's targeted to specific methods.

<!-- Why -->
This allows lines that occupy a disproportionate amount of the total runtime to be quickly identified and investigated.

<!-- We will be covering -->
In this episode we will cover the usage of the line-level profiler `line_profiler`, how your code should be modified to target the profiling and how the output can be interpreted.

## line_profiler

<!-- what is line_profiler, how is it installed -->
[`line_profiler`](https://kernprof.readthedocs.io/en/latest/line_profiler.html#line-profiler-basic-usage) is a line-level profiler which provides both text output and visualisation.

<!--TODO is covering pip here redundant as it's covered in the user setup file? -->
It is not part of the Python standard library, and therefore must be installed via pip.

```sh
pip install line_profiler[all]
```

To use `line_profiler` decorate methods to be profiled with `@profile` which is imported from `line_profiler`.

For example, the below code:

```python
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True
    
print(is_prime(1087))
```

Would be updated to:

```python
from line_profiler import profile

@profile
def is_prime(number):
    if number < 2:
        return False
    for i in range(2, int(number**0.5) + 1):
        if number % i == 0:
            return False
    return True
    
print(is_prime(1087))
```

This tells `line_profiler` to collect metrics for the lines within the method `fizzbuzz()`.
You can still execute your code as normal, and these changes will have no effect.

Similar to the earlier tools, `line_profiler` can then be triggered via `kernprof`.

```sh
python -m kernprof -lvr my_script.py
```

This will output a table per profiled method to console:

```output
Wrote profile results to my_script.py.lprof
Timer unit: 1e-06 s

Total time: 1.65e-05 s
File: my_script.py
Function: is_prime at line 3

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     3                                           @profile
     4                                           def is_prime(number):
     5         1          0.4      0.4      2.4      if number < 2:
     6                                                   return False
     7        32          8.4      0.3     50.9      for i in range(2, int(number**0.5) + 1):
     8        31          7.4      0.2     44.8          if number % i == 0:
     9                                                       return False
    10         1          0.3      0.3      1.8      return True
```

The columns have the following definitions:

| Column | Definition |
|---------|---------------------------------------------------|
| `Line #`  | The line number of the relevant line within the file (specified above the table). |
| `Hits` | The total number of times the line was executed. |
| `Time` | The total time spent executing that line, including child function calls. |
| `Per Hit` | The average time per call, including child function calls (`Time`/`Hits`). |
| `% Time` | The time spent executing the line, including child function calls, relative to the other lines of the function. |
| `Line Contents` | A copy of the line from the file. |

As `line_profiler` must be attached to specific methods and cannot attach to a full Python file or project,
if your Python file has significant code in the global scope it will be necessary to move it into a new method which can then instead be called from global scope.

The profile is also output to file, in this case `my_script.py.lprof`.
This file is not human-readable, but can be printed to console by passing it to `line_profiler`, which will print the same table as above.


```sh
python -m line_profiler -rm my_script.py.lprof
```

## Worked Example

::::::::::::::::::::::::::::::::::::: callout

## Follow Along

<!-- TODO manually write this anchor to add download attribute to the python file? -->
Download the [Python source for the example](episodes/files/line_profiler-worked-example/fizzbuzz.py) and follow along with the worked example on your own machine.

:::::::::::::::::::::::::::::::::::::::::::::

To more clearly demonstrate how to use `line_profiler`, the below implementation of "FizzBuzz" will be line profiled.

```python
n = 100
for i in range(1, n + 1):
    if i % 3 == 0 and i % 5 == 0:
        print("FizzBuzz")
    elif i % 3 == 0:
        print("Fizz")
    elif i % 5 == 0:
        print("Buzz")
    else:
        print(i)
```

As there are no methods, firstly it should be updated to move the code to be profiled into a method:

```python
def fizzbuzz(n):
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

fizzbuzz(n)
```

Next the method can be decorated with `@profile` which must be imported via `line_profiler`:

```python
from line_profiler import profile

@profile
def fizzbuzz(n):
    for i in range(1, n + 1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
        elif i % 3 == 0:
            print("Fizz")
        elif i % 5 == 0:
            print("Buzz")
        else:
            print(i)

fizzbuzz(n)
```

Now that the code has been decorated, it can be profiled!

```sh
python -m kernprof -lvr fizzbuzz.py
```

This will output a table per profiled method to console:

*If you run this locally it should be highlighted due to `-r` passed to `kernprof`.*

```output
Wrote profile results to fizzbuzz.py.lprof
Timer unit: 1e-06 s

Total time: 0.0021535 s
File: fizzbuzz.py
Function: fizzbuzz at line 3

Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     3                                           @profile
     4                                           def fizzbuzz(n):
     5       101         32.5      0.3      1.5      for i in range(1, n + 1):
     6       100         26.9      0.3      1.2          if i % 3 == 0 and i % 5 == 0:
     7         6        125.8     21.0      5.8              print("FizzBuzz")
     8        94         16.7      0.2      0.8          elif i % 3 == 0:
     9        27        541.3     20.0     25.1              print("Fizz")
    10        67         12.4      0.2      0.6          elif i % 5 == 0:
    11        14        285.1     20.4     13.2              print("Buzz")
    12                                                   else:
    13        53       1112.8     21.0     51.7              print(i)
```

For this basic example, we can calculate that "FizzBuzz" would be printed 6 times out of 100, and the profile shows that line 7 (`print("FizzBuzz")` occupied 5.8% of the runtime. This is slightly lower than 6% due to the control flow code (printing to console is expensive relative to the control flow and conditional statements). Similarly, "Fizz" is printed 27 times and occupies 25.1%, likewise "Buzz" is printed 14 times and occupies 13.2%. Each print statement has a similar "Per Hit" time of 20-21 micro seconds.

Therefore it can be seen in this example, how the time spent executing each line matches expectations.

::::::::::::::::::::::::::::::::::::: callout

## Rich Output

The `-r` argument passed to `kernprof` enables rich output, if you run the profile locally it should look similar to this.

![Rich (highlighted) console output provided by `line_profiler` for the above FizzBuzz profile code.](episodes/fig/line_profiler-worked-example.png){alt='A screenshot of the `line_profiler` output from the previous code block, where the code within the line contents column has basic highlighting.'}

:::::::::::::::::::::::::::::::::::::::::::::

## Exercises

The following exercises allow you to review your understanding of what has been covered in this episode.

::::::::::::::::::::::::::::::::::::: challenge 

## Exercise 1: Predator Prey

TODO e.g. decorating a specific function

:::::::::::::::::::::::: hint

- TODO

:::::::::::::::::::::::::::::::::

:::::::::::::::::::::::: solution 

Solution 1: TODO

:::::::::::::::::::::::::::::::::


## Exercise 2: TODO

TODO: e.g. one where there are no functions, so how to decorate

:::::::::::::::::::::::: solution 

Solution 2: TODO

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::



::::::::::::::::::::::::::::::::::::: keypoints

<!-- TODO does this still fit after the content has been written -->
- Specific functions can be line level profiled with `line_profiler` if decorated with `@profile`
- Code in global scope must wrapped if it is to be profiled with `line_profiler`
- The output from `line_profiler` lists the time spent per targeted line of code in descending order.

::::::::::::::::::::::::::::::::::::::::::::::::