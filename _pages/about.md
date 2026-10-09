---
layout: about
title: about
permalink: /

profile:
  align: right
  image: prof_pic.jpg
  image_circular: false # crops the image to make it circular
  more_info: >
    <p>Department of Computer Science</p>
    <p>Stony Brook University</p>
    <p>Stony Brook, NY 11794</p>

selected_papers: true # includes a list of papers marked as "selected={true}"
social: true # includes social icons at the bottom of the page

announcements:
  enabled: true # includes a list of news items
  scrollable: true # adds a vertical scroll bar if there are more than 3 news items
  limit: 5 # leave blank to include all the news in the `_news` folder

latest_posts:
  enabled: false
---

I am a PhD candidate in Computer Science at Stony Brook University and a [MongoDB PhD Fellow](https://www.mongodb.com/company/blog/innovation/announcing-the-2026-mongodb-phd-fellowship-recipients). I am advised by [Michael A. Bender](https://www3.cs.stonybrook.edu/~bender/).

My research focuses on how memory movement and contention limit performance, and on algorithms that overcome those limits. I develop parallel algorithms and space-efficient data structures that combine provable guarantees with high-performance implementations.

In caching, I study miss-ratio curves, caches with limited associativity, and caches with changing capacity. Miss-ratio curves were long considered too expensive to compute in production systems. As part of my MongoDB PhD Fellowship, I am integrating my algorithm into MongoDB, where it computes them with negligible overhead.

Beyond caching, I work on problems whose performance is dominated by memory movement: determinacy race detection in parallel programs, linear sketching for massive, dense graphs, and compact filters.
