---
title: "Introduction to Optimisation"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- Why could optimisation of code be harmful?

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- Able to explain the cost benefit analysis of performing code optimisation

::::::::::::::::::::::::::::::::::::::::::::::::

## Introduction

<!-- Enable you to look at hotspots identified by compiler, identify whether it's efficient -->
Now that you're able to find the most expensive components of your code with profiling, it becomes time to learn how to identify whether that expense is reasonable.

<!-- Necessary to understand how code executes (to a degree) -->
In order to optimise code for performance, it is necessary to have an understanding of what a computer is doing to execute it.

<!-- Goal is to give you a high level understanding of how your code executes. You don't need to be an expert, even a vague general understanding will leave you in a stronger position. -->
Even a high-level understanding of a typical computer architecture, the most common data-structures/algorithms and how Python executes your code, enable the identification of suboptimal approaches. If you have learned to write code informally out of necessity, to get something to work, it's not uncommon to have collected some bad habits along the way.

<!-- This is largely high-level/abstract knowledge applicable to the vast majority of programming languages, applies even more strongly if using compiled Python features like numba -->
The remaining content is often abstract knowledge, that is transferable to the vast majority of programming languages.

## Premature Optimisation

> Programmers waste enormous amounts of time thinking about, or worrying about, the speed of noncritical parts of their programs, and these attempts at efficiency actually have a strong negative impact when debugging and maintenance are considered. We should forget about small efficiencies, say about 97% of the time: **premature optimization is the root of all evil**. Yet we should not pass up our opportunities in that critical 3%. - Donald Knuth

This classic quote among computer scientists states; when considering optimisation it is important to focus on the potential impact, both to the performance and maintainability of the code.

Profiling is a valuable tool in this cause. Should effort be expended to optimise a component which occupies 1% of the runtime? Or would that time be better spent focusing on the mostly components?

Advanced optimisations, mostly outside the scope of this course, can increase the cost of maintenance by obfuscating what code is doing. Even if you are a solo-developer working on private code, your future self should be able to easily comprehend your implementation.

Therefore, the balance between the impact to both performance and maintainability should be considered when optimising code.

This is not to say, don't consider optimisation when first writing code. The selection of appropriate algorithms and data-structures as will be covered is good practice, simply don't fret over a need to micro-optimise every small component of the code that you write.

## Coming Up

In the remainder of this course we will cover:

- todo

<!--
We will cover: 
* 
* How code executes on hardware
    * latency
    * caching
    * branch prediction
* Algorithm/Data-structure selection
   * numpy types vs core python
* data table operations (pandas specific)
* When CPU/GPU/Distributed parallel are appropriate
-->


::::::::::::::::::::::::::::::::::::: keypoints

- The knowledge necessary to perform high-level optimisations of code is largely transferable between programming languages.
- When considering optimisation it is important to focus on the potential impact, both to the performance and maintainability of the code.
- Many high-level optimisations should be considered good-practice.

::::::::::::::::::::::::::::::::::::::::::::::::
