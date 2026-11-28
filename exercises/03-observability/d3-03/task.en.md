---
id: d3-03
title: TCP readiness probe on a Deployment
---
In namespace `d3-03`, add to container `api` of Deployment `api` a **TCP readiness probe** on port
`5678`, every `5` seconds, after `2` seconds. Both replicas must become ready again.
