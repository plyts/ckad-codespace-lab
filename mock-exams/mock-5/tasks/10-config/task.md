---
id: m5-10
title: ConfigMap et Secret
domain: 4
level: examen
context: ckad-b
namespace: m5-10
time: 8
doc: https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/
skill: configmaps
weight: 7
---
Dans le namespace `m5-10` : ConfigMap `agent-cfg` (`LEVEL=warn`) et Secret `agent-sec`
(`TOKEN=s3cr3t-b2`). Pod `agent` (`busybox:1.37`, `sh -c 'sleep 3600'`) qui reçoit la
variable `LOG_LEVEL` depuis `agent-cfg` (clé `LEVEL`) et `API_TOKEN` depuis `agent-sec`
(clé `TOKEN`).
