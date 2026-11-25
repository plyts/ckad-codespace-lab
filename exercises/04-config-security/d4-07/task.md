---
id: d4-07
title: RBAC : Role et RoleBinding
domain: 4
level: avance
context: ckad-a
namespace: d4-07
time: 6
doc: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
skill: rbac
---
Dans le namespace `d4-07`, le ServiceAccount `monitor` doit pouvoir **lire** les Pods
(`get`, `list`, `watch`) et leurs logs (`pods/log`), et rien d'autre.

Crée le Role `pod-reader` et le RoleBinding `monitor-pod-reader`.
