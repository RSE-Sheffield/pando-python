---
title: "Function Level Profiling"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- When is function level profiling appropriate?
- How can `cProfile` and `snakeviz` be used to profile a Python program?
- How are the outputs from function level profiling interpreted?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- execute a Python program via `cProfile` to collect profiling information about a Python program’s execution
- use `snakeviz` to visualise profiling information output by `cProfile`
- interpret `snakeviz` views, to identify the functions where time is being spent during a program’s execution

::::::::::::::::::::::::::::::::::::::::::::::::

## Introduction
<!-- TODO Currently it's a verbatim copy from profiling-introduction.md, there's space for more context in this episode.>

<!-- Context -->
Software is typically comprised of a hierarchy of function calls, both functions written by the developer and those used from the core language and third party packages.

<!-- What -->
Function-level profiling analyses where time is being spent with respect to functions. Typically function-level profiling will calculate the number of times each function is called and the total time spent executing each function, inclusive and exclusive of child function calls.

<!-- Why -->
This allows functions that occupy a disproportionate amount of the total runtime to be quickly identified and investigated.

<!-- We will be covering -->
In this episode we will cover the usage of the function-level profiler `cProfile`, how it's output can be visualised with `snakeviz` and how the output can be interpreted.

## cProfile

<!-- What is cProfile/How is it installed -->
[`cProfile`](https://docs.python.org/3/library/profile.html#instant-user-s-manual) is a function-level profiler provided as part of the Python standard library.

<!-- How is it used? -->
It can be called directly within your Python code as an imported package, however it's easier to use it's script interface:

```sh
python -m cProfile -o <output file> <script name/arguments>
```

For example if you normally run your program as:

```sh
python my_script.py input.csv
```

You would call `cProfile` to produce profiling output `out.prof` with:

```sh
python -m cProfile -o out.prof my_script.py input.csv
```

<!-- yes it's that simple -->
*No additional changes to your code are required, it's really that simple!*


This will produce an output file similar to that shown below:

<!-- TODO is there a better less-abstract example, this one is 're.compile("foo|bar")' ripped from the docs -->

```output
      214 function calls (207 primitive calls) in 0.002 seconds

Ordered by: cumulative time

ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1    0.000    0.000    0.002    0.002 {built-in method builtins.exec}
     1    0.000    0.000    0.001    0.001 <string>:1(<module>)
     1    0.000    0.000    0.001    0.001 __init__.py:250(compile)
     1    0.000    0.000    0.001    0.001 __init__.py:289(_compile)
     1    0.000    0.000    0.000    0.000 _compiler.py:759(compile)
     1    0.000    0.000    0.000    0.000 _parser.py:937(parse)
     1    0.000    0.000    0.000    0.000 _compiler.py:598(_code)
     1    0.000    0.000    0.000    0.000 _parser.py:435(_parse_sub)
```
The columns have the following definitions:

| Column | Definition |
|---------|---------------------------------------------------|
| `ncalls`  | The number of times the given function was called. |
| `tottime` | The total time spent in the given function, excluding child function calls. |
| `percall` | The average tottime per function call (`tottime`/`percall`). |
| `cumtime` | The total time spent in the given function, including child function calls. |
| `percall` | The average cumtime per function call (`cumtime`/`percall`). |
| `filename:lineno(function)` | The location of the given function's definition and it's name. |

This output can be unwieldy to parse for complex programs, so the package `snakeviz` is often utilised to provide an interactive visualisation of the data.


## snakeviz

<!-- what is snakeviz/how is it installed-->
[`snakeviz`](https://jiffyclub.github.io/snakeviz/) is a web browser based graphical viewer for `cProfile` output files.
<!--TODO is covering pip here redundant as it's covered in the user setup file? -->
It is not part of the Python standard library, and therefore must be installed via pip.

```sh
pip install snakeviz
```

Once installed, you can visualise a `cProfile` output file such as `out.prof` via:

```sh
python -m snakeviz out.prof
```
This should open your web browser displaying a page like that below.

![The default visualisation of a `cProfile` output provided by `snakeviz`.](TODO){alt='TODO ALT TEXT'}



## Worked Example

TODO

::::::::::::::::::::::::::::::::::::: challenge 

## Exercise 1: TODO

:::::::::::::::::::::::: solution 

Solution 1: TODO

:::::::::::::::::::::::::::::::::


## Exercise 2: TODO

:::::::::::::::::::::::: solution 

Solution 2: TODO

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::



::::::::::::::::::::::::::::::::::::: keypoints

- A python program can be function level profiled with `cProfile` via `python -m cProfile -o <output file> <script name/arguments>`
- The output file from `cProfile` can be visualised with `snakeviz` via `python -m snakeviz <output file>`
- Function level profiling output displays the nested call hierarchy, listing both the cumulative and total minus sub functions time.

::::::::::::::::::::::::::::::::::::::::::::::::
