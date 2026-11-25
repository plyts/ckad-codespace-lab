---
id: d2-04
title: Rollback après une mise à jour ratée
domain: 2
level: intermediaire
context: ckad-a
namespace: d2-04
time: 4
doc: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
skill: rolling-update
---
Dans le namespace `d2-04`, une mise à jour du Deployment `front` vient d'échouer.
Diagnostique la panne, puis **reviens à la révision précédente** qui fonctionnait.
Tous les réplicas doivent être prêts.
