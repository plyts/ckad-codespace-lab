---
id: d2-03
title: Rolling update with a cause
---
In namespace `d2-03`, update Deployment `front` to image `nginx:1.28-alpine` (container `nginx`),
through a rolling update.

Add to the revision the annotation `kubernetes.io/change-cause` with the value `passage en 1.28`, so
that it shows in `kubectl rollout history`.
