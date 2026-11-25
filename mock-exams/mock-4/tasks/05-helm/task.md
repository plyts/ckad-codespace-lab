---
id: m4-05
title: Mise à jour Helm
domain: 2
level: examen
context: ckad-a
namespace: m4-05
time: 8
doc: https://helm.sh/docs/helm/helm_upgrade/
skill: helm
weight: 7
---
La release Helm `wiki` (chart `~/ckad/m4-05/webapp`) tourne dans le namespace `m4-05`.
Mets-la à jour : `replicaCount=2` et `message=maj`. Puis écris dans
`~/ckad/m4-05/history.txt` la sortie de `helm history wiki`.
