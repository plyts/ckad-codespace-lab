---
id: d3-04
title: CrashLoopBackOff
domain: 3
level: intermediaire
context: ckad-a
namespace: d3-04
time: 5
doc: https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/
skill: debugging
---
Dans le namespace `d3-04`, le Deployment `worker` redémarre en boucle.

1. Écris le **code de sortie** du conteneur dans `~/ckad/d3-04/exit-code.txt`.
2. Corrige le Deployment pour que le conteneur dorme 3600 secondes comme prévu.
