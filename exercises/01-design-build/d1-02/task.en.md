---
id: d1-02
title: Job with several completions
---
In namespace `d1-02`, create a Job named `counter`:

- image `busybox:1.37`, command `sh -c 'echo traitement terminé'`
- it must succeed **3 times** (3 completions), **at most 2 Pods in parallel**
- `backoffLimit` of `2`

The Job must complete successfully.
