---
id: m5-07
title: CrashLoopBackOff
domain: 3
level: examen
context: ckad-b
namespace: m5-07
time: 6
doc: https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/
skill: debugging
weight: 5
---
Dans le namespace `m5-07`, le Deployment `notifier` est en `CrashLoopBackOff`. Lis sa commande :
il attend un fichier. Corrige le Deployment **sans changer sa commande** : monte une
ConfigMap `notifier-config` (clé `ready`, valeur `yes`) sur `/config`.
