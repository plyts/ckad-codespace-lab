---
id: m2-09
title: Ingress à deux chemins
domain: 5
level: examen
context: ckad-a
namespace: m2-09
time: 18
doc: https://kubernetes.io/docs/concepts/services-networking/ingress/
skill: ingress
weight: 20
---
Dans le namespace `m2-09`, crée l'Ingress `home-ing` (classe `traefik`) pour l'hôte `m2.lab.local` :
`/` vers le Service `home` (port 80) et `/docs` vers le Service `docs` (port 9090), en
`pathType: Prefix`.
