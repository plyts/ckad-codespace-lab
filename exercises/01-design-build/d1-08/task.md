---
id: d1-08
title: DaemonSet sur tous les nœuds
domain: 1
level: avance
context: ckad-a
namespace: d1-08
time: 7
doc: https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/
skill: workloads
---
Dans le namespace `d1-08`, crée un DaemonSet `node-agent` (label `app=node-agent`),
image `busybox:1.37`, commande `sh -c 'sleep 3600'`.

Un Pod doit tourner sur **chaque** nœud du cluster, **control-plane compris**.
