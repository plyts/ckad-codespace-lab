---
id: m5-01
title: Job à complétions
domain: 1
level: examen
context: ckad-b
namespace: m5-01
time: 8
doc: https://kubernetes.io/docs/concepts/workloads/controllers/job/
skill: workloads
weight: 7
---
Dans le namespace `m5-01`, crée le Job `migrate` (`busybox:1.37`, `sh -c 'echo migré'`) qui
doit réussir **3 fois**, avec **1** Pods au plus en parallèle et
`backoffLimit: 1`. Il doit être terminé.
