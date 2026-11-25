---
id: d5-04
title: Service sans Endpoints
domain: 5
level: intermediaire
context: ckad-a
namespace: d5-04
time: 5
doc: https://kubernetes.io/docs/concepts/services-networking/service/
skill: services
---
Dans le namespace `d5-04`, le Service `shop` ne répond pas, alors que les Pods du
Deployment `shop` tournent. Corrige **le Service** (pas le Deployment) :
`http://shop.d5-04` doit répondre `shop ok`.
