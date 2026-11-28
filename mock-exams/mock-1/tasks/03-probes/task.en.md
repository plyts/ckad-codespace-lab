---
id: m1-03
title: Readiness and liveness probes
---
In namespace `m1-03`, add to the container of Deployment `catalog`:

- an HTTP **readiness** probe `GET /index.html` port 80, every 5 s;
- a TCP **liveness** probe port 80, after 10 s, every 15 s.
