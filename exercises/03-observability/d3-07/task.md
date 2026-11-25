---
id: d3-07
title: API dépréciées : migrer un manifeste
domain: 3
level: avance
context: ckad-a
namespace: d3-07
time: 7
doc: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
skill: deprecations
---
Le fichier `~/ckad/d3-07/old.yaml` vient d'un vieux cluster : `kubectl apply` le refuse.

Corrige **le fichier lui-même** pour qu'il utilise les versions d'API actuelles, puis
applique-le. Le CronJob `cleanup` et le PodDisruptionBudget `web-pdb` doivent exister
dans le namespace `d3-07`.
