---
id: m3-12
title: NetworkPolicy d'entrée
domain: 5
level: examen
context: ckad-a
namespace: m3-12
time: 12
doc: https://kubernetes.io/docs/concepts/services-networking/network-policies/
skill: networkpolicy
weight: 10
---
Dans le namespace `m3-12`, crée la NetworkPolicy `ledger-access` : les Pods `app=ledger`
n'acceptent du trafic entrant **que** des Pods étiquetés `role=accounting`, sur le port `80`.
Tout le reste est refusé pour ces Pods.
