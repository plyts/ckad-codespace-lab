---
id: d2-05
title: Régler la stratégie de déploiement
domain: 2
level: intermediaire
context: ckad-a
namespace: d2-05
time: 5
doc: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
skill: rolling-update
---
Dans le namespace `d2-05`, modifie le Deployment `api` :

- rolling update qui ne retire **jamais** un Pod avant qu'un nouveau soit prêt
  (`maxUnavailable: 0`) et crée **au plus 1** Pod en plus (`maxSurge: 1`)
- un Pod n'est considéré disponible qu'après **5 secondes** prêt
- garder **4** anciens ReplicaSets au plus
