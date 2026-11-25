---
id: m2-06
title: CrashLoopBackOff : fichier manquant
domain: 3
level: examen
context: ckad-a
namespace: m2-06
time: 7
doc: https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/
skill: debugging
weight: 8
---
Dans le namespace `m2-06`, le Deployment `billing` est en `CrashLoopBackOff`. Lis sa commande :
il attend un fichier. Corrige le Deployment **sans changer sa commande** : monte une
ConfigMap `billing-config` (clé `ready`, valeur `yes`) sur `/config`.
