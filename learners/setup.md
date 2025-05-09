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

If you have `conda` available, you can create and activate a new environment named `py311_env` with Python 3.11 using the following command:

```sh
conda create --name py311_env python=3.11
conda activate py311_env
```

The non-core Python packages required by the course are `pytest`, `snakeviz`, `line_profiler`, `numpy`, `pandas` and `matplotlib` which can be installed via `pip`.
 
```sh
pip install pytest snakeviz line_profiler[all] numpy pandas matplotlib
```

To complete some of the exercises you will need to use a text-editor or Python IDE, so make sure you have your favourite available.

:::::::::::::: instructor

As the instructor, you should additionally install the `shapely` package, which you may need for a brief demo during the episode on scientific Python packages.

```sh
pip install shapely
```

:::::::::::::::::::::::::


:::::::::::::::: spoiler

### Issues installing line_profiler

If you use Zsh as your shell (which is the default on Mac OS), you may come across the error `zsh: no matches found: line_profiler[all]` when installing `line_profiler[all]`.
In Zsh, we need to ensure that the square brackets are treated as standard characters; wrapping them in quotation marks resolves the issue.

```sh
pip install 'line_profiler[all]'
pip install pytest snakeviz numpy pandas matplotlib
```

Alternatively, you can install `line_profiler` via `conda`.

```sh
conda install -c conda-forge line_profiler
```
::::::::::::::::::::::::

:::::::::::::::::::::::::::::::::::::::::::::::::::
