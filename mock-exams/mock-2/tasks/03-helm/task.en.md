---
id: m2-03
title: Helm upgrade
---
Helm release `blog` (chart `~/ckad/m2-03/webapp`) runs in namespace `m2-03`.
Upgrade it: `replicaCount=3` and `message=v2`. Then write the output of
`helm history blog` into `~/ckad/m2-03/history.txt`.
