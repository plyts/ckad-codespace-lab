---
id: m4-02
title: DaemonSet sur tous les nœuds
domain: 1
level: examen
context: ckad-b
namespace: m4-02
time: 8
doc: https://kubernetes.io/docs/concepts/workloads/controllers/daemonset/
skill: workloads
weight: 7
---
Dans le namespace `m4-02`, crée le DaemonSet `log-agent` (`busybox:1.37`, `sh -c 'sleep 3600'`)
qui place un Pod sur **tous** les nœuds du cluster, control-plane compris.
