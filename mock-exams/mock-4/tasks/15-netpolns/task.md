---
id: m4-15
title: NetworkPolicy par namespace
domain: 5
level: examen
context: ckad-a
namespace: m4-15
time: 8
doc: https://kubernetes.io/docs/concepts/services-networking/network-policies/
namespaces: m4-15 m4-15-ops
skill: networkpolicy
weight: 7
---
Dans le namespace `m4-15`, crée la NetworkPolicy `from-m4-15-ops` : les Pods `app=vault`
n'acceptent du trafic entrant que des Pods **du namespace `m4-15-ops`** (n'importe quel Pod).
