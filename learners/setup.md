---
title: Setup
---

<!--
## Data Sets

FIXME: place any data you want learners to use in `episodes/data` and then use
       a relative link ( [data zip file](data/lesson-data.zip) ) to provide a
       link to it, replacing the example.com link.
       
Download the [data zip file](https://example.com/FIXME) and unzip it to your Desktop
-->

## Software Setup

::::::::::::::::::::::::::::::::::::::: discussion

### Details

This course uses Python and was developed using Python 3.11, therefore it is recommended that you have a Python 3.11 or newer environment.

You may want to create a new Python virtual environment for the course, this can be done with your preferred Python environment manager (e.g. `conda`, `pipenv`), the required packages can all be installed via `pip`.

<!-- conda create -n pando python
     conda activate pando -->

The non-core Python packages required by the course are `pytest`, `snakeviz`, `line_profiler`, `numpy`, `pandas` and `matplotlib` which can be installed via `pip`.
 
```sh
pip install pytest snakeviz line_profiler[all] numpy pandas matplotlib
```

To complete some of the exercises you will need to use a text-editor or Python IDE, so make sure you have your favourite available.



:::::::::::::::: spoiler

### Mac OS (line_profiler)

If you are unable to install `line_profiler` via `pip` on MacOS. Instead it can be installed via `conda`.

```sh
conda install line_profiler
```

It may first be necessary to enable conda-forge.

```sh
conda config --add channels conda-forge
```
::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::::::
