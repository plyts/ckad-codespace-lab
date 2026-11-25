---
id: m3-11
title: Ressource personnalisée
domain: 4
level: examen
context: ckad-a
namespace: m3-11
time: 11
doc: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
cleanup: crd/maintenances.ops.m3.lab
skill: crd
weight: 9
---
Une CRD du groupe `ops.m3.lab` est installée. Dans le namespace `m3-11`, crée un objet `Maintenance`
nommé `weekly` avec `spec.window: dimanche 02h`. Écris la liste des ressources de ce groupe
(`kubectl api-resources --api-group=ops.m3.lab`) dans `~/ckad/m3-11/resources.txt`.
