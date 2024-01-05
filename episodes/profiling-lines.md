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

Whilst profiling, you may find that function level profiling highlights 

## line_profiler

## Worked Example

## Exercises

The following exercises allow you to review your understanding of what has been covered in this episode.

::::::::::::::::::::::::::::::::::::: challenge 

## Exercise 1: TODO

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