---
id: m3-06
title: Stratégie Recreate
domain: 2
level: examen
context: ckad-a
namespace: m3-06
time: 7
doc: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
skill: rolling-update
weight: 6
---
Dans le namespace `m3-06`, configure le Deployment `legacy` pour que chaque mise à jour
**arrête tous les anciens Pods avant** de créer les nouveaux (stratégie `Recreate`).
Puis mets-le à jour vers `nginx:1.28-alpine`.
