---
id: m3-05
title: Bascule blue/green
domain: 2
level: examen
context: ckad-b
namespace: m3-05
time: 8
doc: https://kubernetes.io/docs/concepts/services-networking/service/
skill: strategies
weight: 7
---
Dans le namespace `m3-05`, les versions blue et green de `checkout` tournent ; le Service `checkout`
envoie tout à blue. **Bascule** le Service vers green, puis réduis `checkout-blue` à 0 réplica
(sans le supprimer).
