---
id: d2-08
title: Canary à 20 %
domain: 2
level: avance
context: ckad-a
namespace: d2-08
time: 7
doc: https://kubernetes.io/docs/concepts/workloads/management/#canary-deployments
skill: strategies
---
Dans le namespace `d2-08`, le Service `api` envoie le trafic aux 5 Pods de `api-v1`
(labels `app=api`, `track=stable`).

Mets en place un **canary** : environ **20 %** des requêtes doivent aller vers une
nouvelle version, sans changer le Service :

- Deployment `api-v2`, image `hashicorp/http-echo:1.0.0`, argument `-text=api v2`,
  port 5678, labels `app=api` et `track=canary`
- au total **5 Pods** derrière le Service : 4 stables et 1 canary
