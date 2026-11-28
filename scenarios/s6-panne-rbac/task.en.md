---
id: s6-panne-rbac
title: Forbidden: repair a ServiceAccount's permissions
---
**Failure scenario.** Context `ckad-a`, namespace `rapports`.

ServiceAccount `reporter` builds a report on the namespace's Pods and ConfigMaps, but it fails: the
errors are in `~/ckad/s6-panne-rbac/forbidden.log`.

Give it **the minimum** permissions: read (`get`, `list`) the Pods and ConfigMaps of namespace
`rapports`. Role `reporter`, RoleBinding `reporter`.
