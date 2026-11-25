---
id: m5-06
title: Blue/green
domain: 2
level: examen
context: ckad-a
namespace: m5-06
time: 7
doc: https://kubernetes.io/docs/concepts/services-networking/service/
skill: strategies
weight: 6
---
Dans le namespace `m5-06`, les versions blue et green de `profile` tournent ; le Service `profile`
envoie tout à blue. **Bascule** le Service vers green, puis réduis `profile-blue` à 0 réplica
(sans le supprimer).
