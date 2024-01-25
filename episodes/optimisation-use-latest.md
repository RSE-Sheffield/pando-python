---
title: "Keep Python & Packages up to Date"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- Why would a newer version of Python or a package be faster?
- Are there any risks to updating Python and packages?
- How can reproducibility be ensured through package upgrades?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Able to explain why using the latest versions of Python and packages is beneficial.
- Able to identify when updating is not possible due to incompatibilities. 
- Able to ensure code remains reproducible through package changes.

::::::::::::::::::::::::::::::::::::::::::::::::

## Introduction

<!-- Why it's important to use the most recent Python and packages viable -->
It's important to use the latest Python wherever feasible. In addition to new features and fixes, much work has been completed over the lifetime of Python 3 to improve the performance of the language.

> [Python 3.11](https://docs.python.org/3/whatsnew/3.11.html) is between 10-60% faster than Python 3.10. On average, we measured a 1.25x speedup on the standard benchmark suite.

Future proposals, such changes to the [JIT](https://tonybaloney.github.io/posts/python-gets-a-jit.html) and [GIL](https://peps.python.org/pep-0703/) will provide further improvements to performance.

Similarly, major packages particularly those with a performance focus such as NumPy and Pandas should be kept up to date for similar reasons.

<!-- performance regressions for major packages are rare -->
These improvements are often free, requiring minimal changes to any code (unlike the jump from Python 2 to Python 3).

Performance regressions within major packages should be considered rare, they often track performance alongside their test suites.

<!-- Not always possible due to incompatibilities -->
However, the more packages and language features your code touches, and the older the Python it currently uses, the greater chance of incompatibilities making it difficult to upgrade.

<!-- Updates may include breaking changes, important to have validation inplace to ensure results aren't affected -->
When updating, it's important to have tests in place, to validate the correctness of your code.
A single small dependent package could introduce a breaking change.
This could cause your code to crash, or worse subtly change your results.

<!-- This is also good practice when optimising your code, to ensure mistakes aren't made -->
When optimising your code, these tests will come in handy too.
Mistakes are easily introduced when updating code that wasn't written recently, even for experienced programmers, so be sure that they will be found.

## Ensuring Reproducible Results

There are a plethora of methods for testing code. The most common is the package [pytest](https://docs.pytest.org/en/latest/) which provides an easy to use unit testing framework.

Python files containing tests are created, their filename must begin with `test`.

Within this file, any functions that begin `test` are considered tests that can be executed by pytest.

The `assert` keyword is used, to test whether a condition evaluates to `True`.

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

This is only the simplest introduction to using pytest, it has advanced features such as fixtures, mocking and test skipping.
[Pytest's documentation](https://docs.pytest.org/en/latest/how-to/index.html) covers all this and more.

<!-- todo exercise, write a test (suite?) for a provided function, to catch people not handling edge-cases-->


## Updating Python & Packages

<!-- Not as relevant if you are starting from scratch -->
*This isn't as relevant if you're starting from scratch. Simply make sure you've installed the latest Python before you start.*


<!-- todo recommended way, because Python is incredibly bad at this -->

<!-- Worth also mentioning for same reason, to have requirements.txt? -->



::::::::::::::::::::::::::::::::::::: keypoints

- Where feasible, the latest version of Python and packages should be used as they can include significant free improvements to the performance of your code.
- There is a risk that updating Python or packages will not be possible to due to version incompatibilities or will require breaking changes to your code.
- Changes to packages may impact results output by your code, ensure you have a method of validation ready prior to attempting upgrades.

::::::::::::::::::::::::::::::::::::::::::::::::
