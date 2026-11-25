---
id: m4-09
title: Sondes
domain: 3
level: examen
context: ckad-b
namespace: m4-09
time: 6
doc: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
skill: probes
weight: 5
---
Dans le namespace `m4-09`, ajoute au conteneur du Deployment `media` :

- une **readiness** probe HTTP `GET /` port 80, toutes les 5 s ;
- une **liveness** probe TCP port 80, après 10 s, toutes les 15 s.
