---
id: m4-06
title: Canary à 20 %
domain: 2
level: examen
context: ckad-b
namespace: m4-06
time: 7
doc: https://kubernetes.io/docs/concepts/workloads/management/#canary-deployments
skill: strategies
weight: 6
---
Dans le namespace `m4-06`, le Service `pricing` sert 5 Pods `pricing-stable`. Déploie un
canary `pricing-canary` (`hashicorp/http-echo:1.0.0`, `-text=pricing v2`, port 5678, labels
`app=pricing`, `track=canary`) pour que **1 Pod(s) sur 5** derrière le Service
soient en v2. Le nombre total de Pods reste 5.
