---
id: d1-02
title: Job à complétions multiples
domain: 1
level: debutant
context: ckad-a
namespace: d1-02
time: 4
doc: https://kubernetes.io/docs/concepts/workloads/controllers/job/
skill: workloads
---
Dans le namespace `d1-02`, crée un Job nommé `counter` :

- image `busybox:1.37`, commande `sh -c 'echo traitement terminé'`
- il doit réussir **3 fois** (3 complétions), **2 Pods au plus en parallèle**
- `backoffLimit` de `2`

Le Job doit être terminé avec succès.
