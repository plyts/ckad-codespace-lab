---
id: s6-panne-rbac
title: Forbidden : réparer les droits d'un ServiceAccount
domain: 0
level: intermediaire
context: ckad-a
namespace: rapports
time: 8
doc: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
skill: rbac
---
**Scénario de panne.** Contexte `ckad-a`, namespace `rapports`.

Le ServiceAccount `reporter` génère un rapport sur les Pods et les ConfigMaps du namespace,
mais il échoue : les erreurs sont dans `~/ckad/s6-panne-rbac/forbidden.log`.

Donne-lui **le minimum** de droits : lire (`get`, `list`) les Pods et les ConfigMaps du
namespace `rapports`. Role `reporter`, RoleBinding `reporter`.
