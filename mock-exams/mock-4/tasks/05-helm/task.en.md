---
id: m4-05
title: Helm upgrade
---
Helm release `wiki` (chart `~/ckad/m4-05/webapp`) runs in namespace `m4-05`.
Upgrade it: `replicaCount=2` and `message=maj`. Then write the output of
`helm history wiki` into `~/ckad/m4-05/history.txt`.
