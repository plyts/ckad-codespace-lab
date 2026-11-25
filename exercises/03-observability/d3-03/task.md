---
id: d3-03
title: Readiness probe TCP sur un Deployment
domain: 3
level: debutant
context: ckad-a
namespace: d3-03
time: 4
doc: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
skill: probes
---
Dans le namespace `d3-03`, ajoute au conteneur `api` du Deployment `api` une
**readiness probe TCP** sur le port `5678`, toutes les `5` secondes, après `2` secondes.
Les 2 réplicas doivent redevenir prêts.
