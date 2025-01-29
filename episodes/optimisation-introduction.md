---
title: "Introduction to Optimisation"
teaching: 10
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- Why could optimisation of code be harmful?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Able to explain the cost benefit analysis of performing code optimisation

::::::::::::::::::::::::::::::::::::::::::::::::

## Introduction

<!-- Changing the narrative: you'd better learn how to write a good code an what are the good practice -->
Think about optimisation as the first step on your journey to writing high-performance code.
It’s like a race: the faster you can go without taking unnecessary detours, the better. 
Code optmisation is all about understanding the principles of efficiency in Python and being conscious of how small changes can yield massive improvements.
  
<!-- Necessary to understand how code executes (to a degree) -->
These are the first steps in code optimisation: making better choices as you write your code and have an understanding of what a computer is doing to execute it.

<!-- Goal is to give you a high level understanding of how your code executes. You don't need to be an expert, even a vague general understanding will leave you in a stronger position. -->
A high-level understanding of how your code executes, such as how Python and the most common data-structures and algorithms are implemented, can help you identify suboptimal approaches when programming. If you have learned to write code informally out of necessity, to get something to work, it's not uncommon to have collected some bad habits along the way.

<!-- This is largely high-level/abstract knowledge applicable to the vast majority of programming languages, applies even more strongly if using compiled Python features like numba -->
The remaining content is often abstract knowledge, that is transferable to the vast majority of programming languages. This is because the hardware architecture, data-structures and algorithms used are common to many languages and they hold some of the greatest influence over performance bottlenecks.

## Optimising code from scratch: trade-off between performance and maintainability

> Programmers waste enormous amounts of time thinking about, or worrying about, the speed of noncritical parts of their programs, and these attempts at efficiency actually have a strong negative impact when debugging and maintenance are considered. We should forget about small efficiencies, say about 97% of the time: **premature optimisation is the root of all evil**. Yet we should not pass up our opportunities in that critical 3%. - Donald Knuth

This classic quote among computer scientists emphasizes the importance of considering both performance and maintainability when optimizing code. While advanced optimizations may boost performance, they often come at the cost of making the code harder to understand and maintain. Even if you're working alone on private code, your future self should be able to easily understand the implementation. Hence, when optimizing, always weigh the potential impact on both performance and maintainability.

This doesn't mean you should ignore performance when initially writing code. Choosing the right algorithms and data structures, as we’ve discussed in this course, is essential. However, there's no need to obsess over micro-optimizing every tiny component of your code—focus on the bigger picture.

## Ensuring Reproducible Results when optimising an existing code

<!-- This is also good practice when optimising your code, to ensure mistakes aren't made -->
When optimizing existing code, you're often making speculative changes, which can lead to subtle mistakes. To ensure that your optimizations are actually improving the code without introducing errors, it's crucial to have a solid strategy for checking that the results remain correct.

Testing should already be an integral part of your development process. It helps clarify expected behavior, ensures new features are working as intended, and protects against unintended regressions in previously working functionality. Always verify your changes through testing to ensure that the optimizations don’t compromise the correctness of your code.

## pytest Overview

There are a plethora of methods for testing code. Most Python developers use the testing package [pytest](https://docs.pytest.org/en/latest/), it's a great place to get started if you're new to testing code. Tests should be created within a project's testing directory, by creating files named with the form `test_*.py` or `*_test.py`. pytest looks for these files, when running the test suite. Within the created test file, any functions named in the form `test*` are considered tests that will be executed by pytest. The `assert` keyword is used, to test whether a condition evaluates to `True`.

Here's a quick example of how a test can be used to check your function's output against an expected value.

```python
# file: test_demonstration.py

# A simple function to be tested, this could instead be an imported package
def squared(x):
    return x**2

# A simple test case
def test_example():
    assert squared(5) == 24
```

When `py.test` is called inside a working directory, it will then recursively find and execute all the available tests.

```sh
>py.test
================================================= test session starts =================================================
platform win32 -- Python 3.10.12, pytest-7.3.1, pluggy-1.3.0
rootdir: C:\demo
plugins: anyio-4.0.0, cov-4.1.0, xdoctest-1.1.2
collected 1 item

test_demonstration.py F                                                                                          [100%]

====================================================== FAILURES =======================================================
____________________________________________________ test_example _____________________________________________________

    def test_example():
>       assert squared(5) == 24
E       assert 25 == 24
E        +  where 25 = squared(5)

test_demonstration.py:9: AssertionError
=============================================== short test summary info ===============================================
FAILED test_demonstration.py::test_example - assert 25 == 24
================================================== 1 failed in 0.07s ==================================================
```

Whilst not designed for benchmarking, it does provide the total time the test suite took to execute. In some cases this may help identify whether the optimisations have had a significant impact on performance.

This is only the simplest introduction to using pytest, it has advanced features common to other testing frameworks such as fixtures, mocking and test skipping.
[pytest's documentation](https://docs.pytest.org/en/latest/how-to/index.html) covers all this and more.
You may already have a different testing workflow in-place for validating the correctness of the outputs from your code.

::: instructor

* Fixtures: A test fixture is a common class which multiple tests can inherit from. This class will typically include methods that perform common initialisation and teardown actions around the behaviour to be tested. This reduces repeated code.
* Mocking: If you wish to test a feature which would relies on a live or temperamental service, such as making API calls to a website. You can mock that API, so that when the test runs synthetic responses are produced rather than the real API being used.
* Test skipping: You may have configurations of your software that cause certain tests to be unsupported. Skipping allows conditions to be added to tests, to decide whether they should be executed or skipped.

:::


<!-- todo callout FAIR: testing course (when it's ready) -->

<!--
## Coming Up

In the remainder of this course we will cover:

- Data Structures & Algorithms
  - Lists vs Tuples
  - Sets
  - Generator Functions
  - Searching
- Minimise Python Written
    - built-ins
    - NumPY
    - Pandas
- Newer is Often Faster
  - Keeping Python and packages upto date
- How the Computer Hardware Affects Performance
   - How variables are accessed & the performance implications
   - Latency in perspective
   - Memory allocation isn't free
-->

::::::::::::::::::::::::::::::::::::: keypoints

- The knowledge necessary to perform high-level optimisations of code is largely transferable between programming languages.
- When considering optimisation it is important to focus on the potential impact, both to the performance and maintainability of the code.
- Many high-level optimisations should be considered good-practice.

::::::::::::::::::::::::::::::::::::::::::::::::
