---
id: m4-01
title: Pod et manifeste
domain: 1
level: examen
context: ckad-a
namespace: m4-01
time: 8
doc: https://kubernetes.io/docs/concepts/workloads/pods/
skill: workloads
weight: 7
---
Dans le namespace `m4-01`, crée le Pod `edge` (image `nginx:1.28-alpine`, labels `tier=edge,env=prod`, port `80`)
et enregistre son manifeste YAML dans `~/ckad/m4-01/edge.yaml`.
