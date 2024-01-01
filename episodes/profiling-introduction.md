---
title: "Introduction to Profiling"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- TODO

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- explain the benefits of profiling code and different types of profiler
- identify the appropriate Python profiler for a given scenario
- explain how to select an appropriate test case for profiling and why

::::::::::::::::::::::::::::::::::::::::::::::::

## Introduction

<!-- Profiling is (what) -->
Performance profiling is the process of analysing and measuring the performance of a program or script, to understand where time is being spent during execution.

<!-- It can be used for (where) -->
Profiling is useful when you have written any code that will be running for a substantial period of time.
As your code grows in complexity, it becomes increasingly difficult to estimate where time is being spent during execution.
Profiling allows you to narrow down where the time is being spent, to identify whether this is of concern or not.

<!-- This allows enables faster/more (why) -->
Profiling is a relatively quick process which can either provide you the peace of mind that your code is efficient, or highlight the performance bottleneck.
Knowing the bottleneck allows you to optimise it (or more specifically request support in optimising it), potentially leading to significant speedups enabling faster research. In extreme cases, addressing bottlenecks has enabled programs to run hundreds or thousands of times faster!

<!-- Increasingly, concern for green/eco compute and or cloud costs (why) -->
Increasingly, particularly with relation to HPC, attention is being paid to the energy usage of software. Profiling your software will provide you the confidence that your software is an efficient use of resources.


::::::::::::::::::::::::::::::::::::: callout

## All Programmers Can Benefit

<!-- Everyone benefits (why) -->
Even professional programmers make oversights that can lead to poor performance, that can be identified through profiling.

For example Grand Theft Auto Online, which has allegedly earned over $7bn since it's 2013 release, was notorious for it's slow loading times.
8 years after it's release [a 'hacker'](https://nee.lv/2021/02/28/How-I-cut-GTA-Online-loading-times-by-70/) had enough, they reverse engineered and profiled the code to enable a 70% speedup!

*How much revenue did that unnecessary bottleneck cost, through user churn?*

*How much time and energy was wasted, by unnecessarily slow loading screens?*

:::::::::::::::::::::::::::::::::::::::::::::

## Types of Profiler

There are multiple approaches to profiling, most programming languages have one or more tools available covering these approaches.
Whilst these tools differ, their core functionality can be grouped into four categories.

### Manual Profiling

Similar to using `print()` for debugging, manually timing sections of code can provide a rudimentary form of profiling.

```Python
import time

t_a = time.monotonic()
# A: Do something
t_b = time.monotonic()
# B: Do something else
t_c = time.monotonic()
# C: Do another thing
t_d = time.monotonic()

mainTimer_stop = time.monotonic()
print(f"A: {t_b - t_a} seconds")
print(f"B: {t_c - t_b} seconds")
print(f"C: {t_d - t_c} seconds")
```

*Above is only one example of how you could manually profile your Python code, there are many similar techniques.*

Whilst this can be appropriate for profiling narrow sections of code, it becomes increasingly impractical as a project grows in size and complexity.
Furthermore, it's also unproductive to be routinely adding and removing these small changes if they interfere with the required outputs of a project.

::::::::::::::::::::::::::::::::::::: callout

## Benchmarking

You may have previously used [`timeit`](https://docs.python.org/3/library/timeit.html) for timing Python code.

This package returns the **total runtime** of an isolated block of code, without providing a more granular timing breakdown.
Therefore, it is better described as a tool for **benchmarking**.

:::::::::::::::::::::::::::::::::::::::::::::

### Function-Level Profiling
<!-- Context -->
Software is typically comprised of a hierarchy of function calls, both functions written by the developer and those used from the core language and third party packages.

<!-- What -->
Function-level profiling analyses where time is being spent with respect to functions. Typically function-level profiling will calculate the number of times each function is called and the total time spent executing each function, inclusive and exclusive of child function calls.

<!-- Why -->
This allows functions that occupy a disproportionate amount of the total runtime to be quickly identified and investigated.

<!-- We will be covering -->
In this course we will cover the usage of the function-level profiler `cprofile` and how it's output can be visualised with `snakeviz`.

### Line-Level Profiling
<!-- Context -->
Function-level profiling may not always be granular enough, perhaps your software is a single long script, or function-level profiling highlighted a particularly complex function.

<!-- What -->
Line-level profiling provides greater granularity, analysing where time is being spent with respect to individual lines of code. 

<!-- Why -->
This will identify individual lines of code that occupy an disproportionate amount of the total runtime.

<!-- Caveat (too early to introduce this?) -->
<!-- Typically, function-level profiling should be attempted first as it has a greater signal-to-noise ratio and is often significantly cheaper to perform. -->

<!-- We will be covering -->
In this course we will cover the usage of the line-level profiler `line_profiler`.

### Timeline Profiling
<!-- Context -->
Timeline profiling takes a different approach to visualising where time is being spent during execution.

<!-- What -->
Typically a subset of function-level profiling, the execution of the profiled software is instead presented as a timeline highlighting the order of function execution in addition to the time spent in each individual function call.

<!-- Why -->
By highlighting individual functions calls patterns relating to how performance scales over time can be identified. These would be hidden with the aforementioned aggregate approaches.

<!-- We will be covering -->
In this course we will cover the usage of the timeline profiler `viztracer`.

### Hardware Metric Profiling

Processor manufacturers typically release advanced profilers specific to their hardware with access to internal hardware metrics.
These profilers can provide analysis of performance relative to theoretical hardware maximums (e.g. memory bandwidth or mathematical operations per second) and detail the utilisation of specific hardware features and operations.

Using these hardware specific profilers requires an advanced understanding of the relevant processor architecture and may lead to hardware specific optimisations.

Example of these profilers include; Intel's VTune, AMD's uProf, and NVIDIA's Nsight Compute.

Profiling of this nature is outside the scope of this course and not typically appropriate for Python code.


## Selecting an appropriate Test Case

<!-- Todo, how to frame data-set selection -->






::::::::::::::::::::::::::::::::::::: discussion

# Exercise (5 minutes)

Think about a project where you've been working with Python.
Do you know where the time during execution is being spent?

Write a short plan of the approach you would take to investigate and confirm
where the majority of time is being spent during it's execution.

<!-- TODO should they share this anywhere, should it be discussed within the group? -->

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: hint

- What tools and techniques would be required?
- Is there a clear priority to these approaches?
- Which test-case/s would be appropriate?

::::::::::::::::::::::::::::::::::::::::::::::::


::::::::::::::::::::::::::::::::::::: keypoints

todo summarise lessons learned

::::::::::::::::::::::::::::::::::::::::::::::::