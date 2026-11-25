---
id: m1-03
title: Sondes readiness et liveness
domain: 3
level: examen
context: ckad-a
namespace: m1-03
time: 9
doc: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
skill: probes
weight: 15
---
Dans le namespace `m1-03`, ajoute au conteneur du Deployment `catalog` :

- une **readiness** probe HTTP `GET /index.html` port 80, toutes les 5 s ;
- une **liveness** probe TCP port 80, après 10 s, toutes les 15 s.
