---
id: m1-01
title: Sidecar de journalisation
domain: 1
level: examen
context: ckad-a
namespace: m1-01
time: 12
doc: https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/
skill: multi-container
weight: 20
---
Dans le namespace `m1-01`, crée le Pod `audit` avec un volume `emptyDir` partagé monté sur
`/var/audit` :

- conteneur `writer` (`busybox:1.37`) :
  `sh -c 'while true; do echo "event $(date)" >> /var/audit/out.log; sleep 2; done'`
- **sidecar natif** `reader` (`busybox:1.37`) : `sh -c 'tail -F /var/audit/out.log'`
