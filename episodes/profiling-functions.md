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

<!-- TODO should the remainder of this section be in a call-out, it's unnecessary -->
If you instead, don't specify output to file (e.g. remove `-o out.prof` from the command), `cProfile` will produce output to console similar to that shown below:

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

This output can often exceed the terminal's buffer length for large programs and can be unwieldy to parse, so the package `snakeviz` is often utilised to provide an interactive visualisation of the data when exported to file.


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
This should open your web browser displaying a page similar to that below.

![An example of the default 'icicle' visualisation provided by `snakeviz`.](episodes/fig/snakeviz-home.png){alt='A web page, with a central diagram representing a call-stack, with the root at the top and the horizontal axis representing the duration of each call. Below this diagram is the top of a table detailing the statistics of individual methods.'}

<!-- From SnakeViz docs
In the icicle visualization style functions are represented by rectangles. A root function is the top-most rectangle, with functions it calls below it, then the functions those call below them, and so on. The amount of time spent inside a function is represented by the width of the rectangle. A rectangle that stretches across most of the visualization represents a function that is taking up most of the time of its calling function, while a skinny rectangle represents a function that is using hardly any time at all.
-->

The icicle diagram displayed by `snakeviz` represents the call stack during the execution of the profiled code.
The box which fills the top row represents the the root call, filling the row shows that it occupied 100% of the runtime.
The second row holds the child methods called from the root, with their widths relative to the proportion of runtime they occupied.
This continues with each subsequent row, however where a method only occupies 50% of the runtime, it's children can only occupy a maximum of that runtime hence the appearance of "icicles".

By clicking a box within the diagram, it will "zoom" making the selected box the root allowing more detail to be explored. The diagram is limited to 10 rows by default ("Depth") and methods with a relatively small proportion of the runtime are hidden ("Cutoff").

As you hover each box, information to the left of the diagram updates specifying the location of the method and for how long it ran.

## Worked Example

::::::::::::::::::::::::::::::::::::: callout

## Follow Along

<!-- TODO manually write this anchor to add download attribute to the python file? -->
Download the [Python source for the example](episodes/files/snakeviz-worked-example/example.py) or [`cProfile` output file](episodes/files/snakeviz-worked-example/out.prof) and follow along with the worked example on your own machine.

```sh
python -m cProfile -o out.prof example.py
python -m snakeviz out.prof
```

:::::::::::::::::::::::::::::::::::::::::::::

To more clearly demonstrate how an execution hierarchy maps to the icicle diagram, the below toy example Python script has been implemented.

```python
import time

def a_1():
    for i in range(3):
        b_1()
    time.sleep(1)
    b_2()
    
def b_1():
    c_1()
    c_2()

def b_2():
    time.sleep(1)
    
def c_1():
    time.sleep(0.5)

def c_2():
    time.sleep(0.3)
    d_1()

def d_1():
    time.sleep(0.1)

# Entry Point
a_1()
```

All of the methods except for `b_1()` call `time.sleep()`, this is used to provide synthetic bottlenecks to create an interesting profile.

* `a_1()` calls `b_1()` x3 and `b_2()` x1
* `b_1()` calls `c_1()` x1 and `c_2()` x1
* `c_2()` calls `d_1()`

<!-- TODO: Alt text here is redundant? -->
![An icicle visualisation provided by `snakeviz` for the above Python code.](episodes/fig/snakeviz-worked-example-icicle.png){alt='The snakeviz icicle visualisation for the worked example Python code.'}

The third row represents `a_1()`, the only method called from global scope, therefore the first two rows represent Python's internal code for launching our script and can be ignored (by clicking on the third row).

The row following `a_1()` is split into three boxes representing `b_1()`, `time.sleep()` and `b_2()` in the order they were first called. Note that `b_1()` is called three times, but only has one box within the icicle diagram.

If the box for `time.sleep()` is hovered it will change colour along with several other boxes that represent the other locations that `time.sleep()` was called from. Note that each of these boxes display the same duration, the timing statistics collected by `cProfile` (and visualised by `snakeviz`) are aggregate, so there is no information about individual method calls for methods which were called multiple times. This does however mean that if you check the properties to the left of the diagram whilst hovering `time.sleep()` you will see a cumulative time of 99% reported, the overhead of the method calls and for loop is insignificant in contrast to the time spent sleeping!

*Below are the properties shown, the time may differ if you generated the profile yourself.*

* **Name:** `<built-in method time.sleep>`
* **Cumulative Time:** `4.71 s (99.99 %)`
* **File:** `~`
* **Line:** `0`
* **Directory:**

As `time.sleep()` is a core Python method it is displayed as "built-in method" and doesn't have a file, line or directory.

If you hover any boxes representing the methods from the above code, you will see file and line properties completed. The directory property remains empty as the profiled code was in the root of the working directory. A profile of a large project with many files across multiple directories will see this filled.

Find the box representing `c_2()` on the icicle diagram, it's children are unlabelled because they are not wide enough (but they can still be hovered). Clicking `c_2()` zooms in the diagram, showing the children to be `time.sleep()` and `d_1()`.

To zoom back out you can either click the top row, which will zoom out one layer, or click "Reset Zoom" on the left-hand side.

In this simple example the execution is fairly evenly balanced between all of the user-defined methods, so there is not a clear hot-spot to investigate.

::::::::::::::::::::::::::::::::::::: callout

## Sunburst

Snakeviz provides an alternate "Sunburst" visualisation, accessed via the "Style" drop-down on the left-hand side.

This provides the same information as "Icicle", however the rows are instead circular with the root method call found at the center.

The sunburst visualisation displays less text on the boxes, so it can be harder to interpret.

<!-- TODO: Alt text here is redundant? -->
![An sunburst visualisation provided by `snakeviz` for the worked example's Python code.](episodes/fig/snakeviz-worked-example-sunburst.png){alt='The snakeviz sunburst visualisation for the worked example Python code.'}

:::::::::::::::::::::::::::::::::::::::::::::

The following exercises allow you to review your understanding of what has been covered in this episode.

::::::::::::::::::::::::::::::::::::: challenge 

## Exercise 1: TODO

Download and profile [this]() Python program, try to locate the function call(s) where the majority of execution time is being spent.

The program can be executed via `python snakeviz_1.py <int>`.
The value of `int` should be in the inclusive range `[0, 100]`, larger numbers take longer to run.

:::::::::::::::::::::::: hint

- If a hotspot isn't visible with `int==0`, try increasing the value.
- If you think you identified the hotspot with your first profile, try investigating how the value of `int` affects the hotspot within the profile.

:::::::::::::::::::::::::::::::::

:::::::::::::::::::::::: solution 

Solution 1: TODO

:::::::::::::::::::::::::::::::::


## Exercise 2: TODO

Example algorithm, with a (hidden) synthetic bottleneck, which leads to a complex function. (to lead into the next episode)

:::::::::::::::::::::::: solution 

Solution 2: TODO

:::::::::::::::::::::::::::::::::
::::::::::::::::::::::::::::::::::::::::::::::::



::::::::::::::::::::::::::::::::::::: keypoints

- A python program can be function level profiled with `cProfile` via `python -m cProfile -o <output file> <script name/arguments>`
- The output file from `cProfile` can be visualised with `snakeviz` via `python -m snakeviz <output file>`
- Function level profiling output displays the nested call hierarchy, listing both the cumulative and total minus sub functions time.

::::::::::::::::::::::::::::::::::::::::::::::::
