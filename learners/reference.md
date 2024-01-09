---
title: 'Reference'
---

## Glossary

Benchmarking
: The process of running a program in order to assess it's overall performance. This can be useful to confirm the impact of optimisations.

Bottleneck
: The component with the lowest throughput, which limits performance of the overall program. Improving the throughput of this component should improve the overall performance.

*Bottleneck is a synonym of limiting factor.*

`cProfile`
: A function level profiler provided by the Python standard library.

Hot Path
: The parts of the code that are executed very frequently during normal operation.

Latency
: The time taken for an operation to complete.

Limiting Factor
: The component with the lowest throughput, which limits performance of the overall program. Improving the throughput of this component should improve the overall performance.

*Limiting factor is a synonym of bottleneck.*

`line_profiler`
: A line level profiler for Python that can be installed via `pip`.

Profiling
: The measuring and analysis of granular performance metrics of a program, to understand where time is being spent during execution. Typically used to prioritise optimisation.

`snakeviz`
: A web-browser based visualisation tool for `cProfile` outputs that can be installed via `pip`.

`viztracer`
: A timeline profiler for Python that can be installed via `pip`.
