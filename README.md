# Profiling & Optimisation (Python)

## Introduction

This lesson introduces the basics of profiling and optimising Python code. The course is designed to be accessible to Python users of all skill levels (beyond total beginner). The optimisations presented should be considered performance best practices, they are demonstrated with small programming patterns that demonstrate multiple approaches in code to achieve the same result with differing performance.

## Contact Us

This course was originally authored by [@Robadob](https://github.com/Robadob) and is now also maintained by [@JostMigenda](https://github.com/JostMigenda).

Releases prior to Beta, exist in the original [University of Sheffield repository](https://github.com/RSE-Sheffield/pando-python), which includes custom branding. Please direct issues with course content to the [Carpentries Incubator repository](https://github.com/carpentries-incubator/pando-python).

## Contributing

See [Contributing](CONTRIBUTING.md)

## Acknowledgements

The initial development of this course was funded by the University of Sheffield, to support training initiatives for users of their [Stanage HPC cluster](https://docs.hpc.shef.ac.uk/en/latest/stanage/index.html).

## Building the Site Locally

If you are making complex changes, and wish to build the site locally the below instructions can be followed.


### Setup

Both of these steps should be followed within `rterm`.

```r
# Setup mirrors
options(repos = c(
  carpentries = "https://carpentries.r-universe.dev/", 
  CRAN = "https://cran.rstudio.com/"
))
# Setup install from github
install.packages("devtools")
library(devtools)
# Install Uni of Shef Varnish theme
install_github("RSE-Sheffield/uos-varnish")
# Install remaining official carpentries packages
install.packages(c("sandpaper", "tinkr", "pegboard"))
```
## Development Server

```r
sandpaper::serve()
```
