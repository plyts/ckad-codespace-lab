---
id: m2-04
title: Canary à 25 %
domain: 2
level: examen
context: ckad-a
namespace: m2-04
time: 9
doc: https://kubernetes.io/docs/concepts/workloads/management/#canary-deployments
skill: strategies
weight: 10
---
Dans le namespace `m2-04`, le Service `search` sert 4 Pods `search-stable`. Déploie un
canary `search-canary` (`hashicorp/http-echo:1.0.0`, `-text=search v2`, port 5678, labels
`app=search`, `track=canary`) pour que **1 Pod(s) sur 4** derrière le Service
soient en v2. Le nombre total de Pods reste 4.
