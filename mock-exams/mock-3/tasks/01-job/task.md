---
id: m3-01
title: Job parallèle
domain: 1
level: examen
context: ckad-a
namespace: m3-01
time: 8
doc: https://kubernetes.io/docs/concepts/workloads/controllers/job/
skill: workloads
weight: 7
---
Dans le namespace `m3-01`, crée le Job `resize` (`busybox:1.37`, `sh -c 'echo redimensionné'`) qui
doit réussir **4 fois**, avec **2** Pods au plus en parallèle et
`backoffLimit: 1`. Il doit être terminé.
