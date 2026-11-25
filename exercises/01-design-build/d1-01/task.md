---
id: d1-01
title: Premier Pod nginx
domain: 1
level: debutant
context: ckad-a
namespace: d1-01
time: 3
doc: https://kubernetes.io/docs/concepts/workloads/pods/
skill: workloads
---
Dans le namespace `d1-01`, crée un Pod nommé `web` :

- image `nginx:1.27-alpine`
- label `app=web`
- port de conteneur `80`

Le Pod doit être `Running` et prêt.
