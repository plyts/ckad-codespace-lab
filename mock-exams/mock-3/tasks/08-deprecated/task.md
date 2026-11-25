---
id: m3-08
title: Ingress en API retirée
domain: 3
level: examen
context: ckad-a
namespace: m3-08
time: 8
doc: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
skill: deprecations
weight: 7
---
`~/ckad/m3-08/ingress.yaml` utilise une API retirée. Convertis **le fichier** vers
`networking.k8s.io/v1` (pathType `Prefix`), puis applique-le : `legacy.m3.lab.local` doit répondre `web ok`.
