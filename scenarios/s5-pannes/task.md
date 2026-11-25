---
id: s5-pannes
title: Trois pannes à réparer
domain: 0
level: avance
context: ckad-a
namespace: pannes
time: 15
doc: https://kubernetes.io/docs/tasks/debug/debug-application/
skill: debugging
---
**Scénario de pannes.** Contexte `ckad-a`, namespace `pannes`. Trois composants sont cassés.
Diagnostique chacun avec `get`, `describe`, `events` et `logs`, puis répare :

1. le Deployment `orders` ne démarre pas : il doit lire `DB_HOST` dans la ConfigMap
   `orders-config` (corrige **la ConfigMap**, pas le Deployment) ;
2. le Service `payments` ne répond pas : `http://payments.pannes` doit répondre `payments ok` ;
3. le Pod `uploader` reste `Pending` : son PVC `uploads` (50Mi) doit utiliser la StorageClass
   qui existe dans le cluster.
