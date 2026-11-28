---
id: m4-09
title: Probes
---
In namespace `m4-09`, add to the container of Deployment `media`:

- an HTTP **readiness** probe `GET /` port 80, every 5 s;
- a TCP **liveness** probe port 80, after 10 s, every 15 s.
