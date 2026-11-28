---
id: m5-05
title: Rolling update
---
In namespace `m5-05`, update Deployment `portal` to `nginx:1.28-alpine` (container `nginx`) with the
cause `montée de version` visible in `kubectl rollout history`. Then scale it to **4 replicas**.
