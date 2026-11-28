---
id: m3-01
title: Parallel Job
---
In namespace `m3-01`, create Job `resize` (`busybox:1.37`, `sh -c 'echo redimensionné'`) which must succeed
**4 times**, with at most **2** Pods in parallel and `backoffLimit: 1`. It
must complete.
