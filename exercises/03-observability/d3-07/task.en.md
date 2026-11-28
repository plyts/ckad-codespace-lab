---
id: d3-07
title: Deprecated APIs: migrate a manifest
---
File `~/ckad/d3-07/old.yaml` comes from an old cluster: `kubectl apply` rejects it.

Fix **the file itself** so that it uses the current API versions, then apply it. CronJob `cleanup`
and PodDisruptionBudget `web-pdb` must exist in namespace `d3-07`.
