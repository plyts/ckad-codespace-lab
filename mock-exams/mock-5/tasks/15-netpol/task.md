---
id: m5-15
title: NetworkPolicy
domain: 5
level: examen
context: ckad-b
namespace: m5-15
time: 8
doc: https://kubernetes.io/docs/concepts/services-networking/network-policies/
skill: networkpolicy
weight: 7
---
Dans le namespace `m5-15`, crée la NetworkPolicy `secrets-api-access` : les Pods `app=secrets-api`
n'acceptent du trafic entrant **que** des Pods étiquetés `access=granted`, sur le port `80`.
Tout le reste est refusé pour ces Pods.
