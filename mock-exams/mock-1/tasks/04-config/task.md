---
id: m1-04
title: ConfigMap et Secret en variables
domain: 4
level: examen
context: ckad-a
namespace: m1-04
time: 8
doc: https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/
skill: configmaps
weight: 13
---
Dans le namespace `m1-04` : ConfigMap `worker-cfg` (`LEVEL=debug`) et Secret `worker-sec`
(`TOKEN=t0k3n-a1`). Pod `worker` (`busybox:1.37`, `sh -c 'sleep 3600'`) qui reçoit la
variable `LOG_LEVEL` depuis `worker-cfg` (clé `LEVEL`) et `API_TOKEN` depuis `worker-sec`
(clé `TOKEN`).
