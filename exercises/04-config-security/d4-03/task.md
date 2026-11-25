---
id: d4-03
title: ServiceAccount dédié
domain: 4
level: debutant
context: ckad-a
namespace: d4-03
time: 3
doc: https://kubernetes.io/docs/tasks/configure-pod-container/configure-service-account/
skill: serviceaccounts
---
Dans le namespace `d4-03`, crée le ServiceAccount `deployer`, puis le Pod `tool`
(image `busybox:1.37`, `sh -c 'sleep 3600'`) qui l'utilise. Le jeton du ServiceAccount
ne doit **pas** être monté automatiquement dans ce Pod.
