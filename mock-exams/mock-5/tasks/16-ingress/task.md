---
id: m5-16
title: Ingress
domain: 5
level: examen
context: ckad-a
namespace: m5-16
time: 7
doc: https://kubernetes.io/docs/concepts/services-networking/ingress/
skill: ingress
weight: 6
---
Dans le namespace `m5-16`, crée l'Ingress `front-ing` (classe `traefik`) pour l'hôte `m5.lab.local` :
`/` vers le Service `front` (port 80) et `/api` vers le Service `api` (port 9090), en
`pathType: Prefix`.
