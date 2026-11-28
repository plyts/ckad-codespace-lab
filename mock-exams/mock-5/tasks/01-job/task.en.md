---
id: m5-01
title: Job with completions
---
In namespace `m5-01`, create Job `migrate` (`busybox:1.37`, `sh -c 'echo migré'`) which must succeed
**3 times**, with at most **1** Pods in parallel and `backoffLimit: 1`. It
must complete.
