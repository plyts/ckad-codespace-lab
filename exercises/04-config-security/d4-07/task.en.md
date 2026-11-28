---
id: d4-07
title: RBAC: Role and RoleBinding
---
In namespace `d4-07`, ServiceAccount `monitor` must be able to **read** Pods (`get`, `list`, `watch`)
and their logs (`pods/log`), and nothing else.

Create Role `pod-reader` and RoleBinding `monitor-pod-reader`.
