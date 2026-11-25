---
id: m5-09
title: API retirée
domain: 3
level: examen
context: ckad-a
namespace: m5-09
time: 6
doc: https://kubernetes.io/docs/reference/using-api/deprecation-guide/
skill: deprecations
weight: 5
---
`~/ckad/m5-09/ingress.yaml` utilise une API retirée. Convertis **le fichier** vers
`networking.k8s.io/v1` (pathType `Prefix`), puis applique-le : `old.m5.lab.local` doit répondre `web ok`.
