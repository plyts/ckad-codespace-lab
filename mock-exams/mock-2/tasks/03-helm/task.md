---
id: m2-03
title: Mise à jour Helm
domain: 2
level: examen
context: ckad-b
namespace: m2-03
time: 9
doc: https://helm.sh/docs/helm/helm_upgrade/
skill: helm
weight: 10
---
La release Helm `blog` (chart `~/ckad/m2-03/webapp`) tourne dans le namespace `m2-03`.
Mets-la à jour : `replicaCount=3` et `message=v2`. Puis écris dans
`~/ckad/m2-03/history.txt` la sortie de `helm history blog`.
