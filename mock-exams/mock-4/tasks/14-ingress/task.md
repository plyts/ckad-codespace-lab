---
id: m4-14
title: Ingress
domain: 5
level: examen
context: ckad-b
namespace: m4-14
time: 8
doc: https://kubernetes.io/docs/concepts/services-networking/ingress/
skill: ingress
weight: 7
---
Dans le namespace `m4-14`, crée l'Ingress `shop-ing` (classe `traefik`) pour l'hôte `m4.lab.local` :
`/` vers le Service `shop` (port 80) et `/cart` vers le Service `cart` (port 9090), en
`pathType: Prefix`.
