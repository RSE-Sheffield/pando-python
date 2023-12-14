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
<!-- It can be used for (where) -->
<!-- This allows enables faster/more (why)-->
<!-- It can be difficult to know without profiling, surprise speedup (why2) -->
<!-- Increasingly, concern for green/eco compute and or cloud costs (why3) -->

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

You may have previously used [`timeit`](https://docs.python.org/3/library/timeit.html) for timing Python code.

This package returns the **total runtime** of an isolated block of code, without providing a more granular timing breakdown.
Therefore, it is better described as a tool for **benchmarking**.

:::::::::::::::::::::::::::::::::::::::::::::

### Function-Level Profiling
### Line-Level Profiling
### Hardware Metric Profiling
<!-- "Hardware" metric profilers also exist, but atypical for high-level languages like Python, so won't be covering. -->

## 

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