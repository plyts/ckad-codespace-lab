---
id: d2-03
title: Rolling update avec motif
domain: 2
level: debutant
context: ckad-a
namespace: d2-03
time: 4
doc: https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
skill: rolling-update
---
Dans le namespace `d2-03`, mets à jour le Deployment `front` vers l'image
`nginx:1.28-alpine` (conteneur `nginx`), par rolling update.

Ajoute à la révision l'annotation `kubernetes.io/change-cause` avec la valeur
`passage en 1.28`, pour qu'elle apparaisse dans `kubectl rollout history`.
