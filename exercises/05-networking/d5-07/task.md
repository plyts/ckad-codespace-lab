---
id: d5-07
title: NetworkPolicy en sortie (egress)
domain: 5
level: avance
context: ckad-a
namespace: d5-07
time: 8
doc: https://kubernetes.io/docs/concepts/services-networking/network-policies/
namespaces: d5-07 d5-07-db
skill: networkpolicy
---
Dans le namespace `d5-07`, crée la NetworkPolicy `client-egress` qui s'applique aux
Pods `app=client` et ne les laisse sortir **que** vers :

- les Pods `app=db` du namespace `d5-07-db`, port TCP `80`
- le DNS du cluster (port `53`, UDP et TCP)

Tout autre trafic sortant de ces Pods (par exemple vers `web.d5-07`) doit être bloqué.
