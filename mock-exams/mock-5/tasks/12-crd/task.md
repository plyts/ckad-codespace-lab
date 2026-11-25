---
id: m5-12
title: CRD
domain: 4
level: examen
context: ckad-b
namespace: m5-12
time: 7
doc: https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/
cleanup: crd/pipelines.data.m5.lab
skill: crd
weight: 6
---
Une CRD du groupe `data.m5.lab` est installée. Dans le namespace `m5-12`, crée un objet `Pipeline`
nommé `nightly-etl` avec `spec.source: s3-bucket`. Écris la liste des ressources de ce groupe
(`kubectl api-resources --api-group=data.m5.lab`) dans `~/ckad/m5-12/resources.txt`.
