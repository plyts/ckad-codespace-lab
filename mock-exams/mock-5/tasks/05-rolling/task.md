---
id: m5-05
title: Rolling update
domain: 2
level: examen
context: ckad-a
namespace: m5-05
time: 8
doc: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
skill: rolling-update
weight: 7
---
Dans le namespace `m5-05`, mets à jour le Deployment `portal` vers `nginx:1.28-alpine`
(conteneur `nginx`) avec le motif `montée de version` visible dans `kubectl rollout history`.
Puis passe-le à **4 réplicas**.
