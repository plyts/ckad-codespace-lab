---
id: s5-pannes
title: Three failures to repair
---
**Failure scenario.** Context `ckad-a`, namespace `pannes`. Three components are broken.
Diagnose each with `get`, `describe`, `events` and `logs`, then repair:

1. Deployment `orders` does not start: it must read `DB_HOST` from ConfigMap `orders-config` (fix
   **the ConfigMap**, not the Deployment);
2. Service `payments` does not answer: `http://payments.pannes` must answer `payments ok`;
3. Pod `uploader` stays `Pending`: its PVC `uploads` (50Mi) must use the StorageClass that exists in
   the cluster.
