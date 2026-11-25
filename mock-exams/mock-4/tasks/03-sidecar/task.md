---
id: m4-03
title: Sidecar natif
domain: 1
level: examen
context: ckad-a
namespace: m4-03
time: 7
doc: https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/
skill: multi-container
weight: 6
---
Dans le namespace `m4-03`, crée le Pod `trail` avec un volume `emptyDir` partagé monté sur
`/trail` :

- conteneur `writer` (`busybox:1.37`) :
  `sh -c 'while true; do echo "trace $(date)" >> /trail/out.log; sleep 2; done'`
- **sidecar natif** `reader` (`busybox:1.37`) : `sh -c 'tail -F /trail/out.log'`
