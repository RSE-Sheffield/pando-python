---
title: "Understanding How Code Executes"
teaching: 0
exercises: 0
---

:::::::::::::::::::::::::::::::::::::: questions

- 

::::::::::::::::::::::::::::::::::::::::::::::::

::::::::::::::::::::::::::::::::::::: objectives

- 

::::::::::::::::::::::::::::::::::::::::::::::::

## How is Data Represented in Memory

<!-- Integer 1 byte vs 8 bytes, where does python stand? -->
<!-- Float, where does python stand? -->
<!-- Explicit numpy types -->
<!-- Strings -->

## Accessing Disk

<!-- Read data from a file it goes disk->disk cache->ram->cpu cache->cpu -->

### Latency big picture

<!-- classic latency comparison -->

<!-- Much of the cost is the initiation of the action, so reading 200x1mb file is worse than 1x200mb file. -->

## Accessing Variables

<!-- Read/operate on variable ram->cpu cache->registers->cpu -->

### Avoiding Cache Misses

<!-- Data is moved between ram and cpu cache in cache lines, e.g. 64 bits for all current intel processors (16 int) -->

<!-- Therefore, reading 16 integers contiguously stored in memory should be faster than 16 scattered integers-->

<!-- However alignment matters, cache lines if they are not aligned within the array it could straddle two cache lines rather than one. -->

## Memory allocation is not free

<!-- Even "garbage collected" languages like Python have a cost. -->

## Branch prediction

::::::::::::::::::::::::::::::::::::: keypoints

- 

::::::::::::::::::::::::::::::::::::::::::::::::
