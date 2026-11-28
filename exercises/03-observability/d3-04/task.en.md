---
id: d3-04
title: CrashLoopBackOff
---
In namespace `d3-04`, Deployment `worker` keeps restarting.

1. Write the container's **exit code** into `~/ckad/d3-04/exit-code.txt`.
2. Fix the Deployment so that the container sleeps 3600 seconds as intended.
