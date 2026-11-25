---
id: m1-02
title: Mise à jour avec motif
domain: 2
level: examen
context: ckad-a
namespace: m1-02
time: 12
doc: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
skill: rolling-update
weight: 20
---
Dans le namespace `m1-02`, mets à jour le Deployment `storefront` vers `nginx:1.28-alpine`
(conteneur `nginx`) avec le motif `nginx 1.28` visible dans `kubectl rollout history`.
Puis passe-le à **4 réplicas**.
