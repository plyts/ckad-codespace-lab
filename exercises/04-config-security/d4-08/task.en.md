---
id: d4-08
title: Use a custom resource (CRD)
---
A backup operator installed a custom resource in the cluster.

1. Find its name, group and version (`kubectl api-resources`, `kubectl explain`).
2. In namespace `d4-08`, create an object of that type named `nightly`, with
   `schedule: "0 2 * * *"` and `retention: 7`.
