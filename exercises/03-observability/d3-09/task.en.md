---
id: d3-09
title: Exam-style: misconfigured probes
---
*Exam-style task — 8 minutes.* Context `ckad-a`, namespace `d3-09`.

The Pods of Deployment `orders` keep restarting.

1. Write into `~/ckad/d3-09/cause.txt` the event message explaining the restarts (one line is
   enough).
2. Fix the **liveness probe** so that it targets the application's right port.
3. Add a **startup probe** HTTP `GET /` on that same port, `failureThreshold: 10`,
   `periodSeconds: 2`.
