---
id: d4-08
title: Utiliser une ressource personnalisée (CRD)
domain: 4
level: avance
context: ckad-a
namespace: d4-08
time: 6
doc: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
cleanup: crd/backups.lab.ckad.io
skill: crd
---
Un opérateur de sauvegarde a installé une ressource personnalisée dans le cluster.

1. Trouve son nom, son groupe et sa version (`kubectl api-resources`, `kubectl explain`).
2. Dans le namespace `d4-08`, crée un objet de ce type nommé `nightly`, avec
   `schedule: "0 2 * * *"` et `retention: 7`.
