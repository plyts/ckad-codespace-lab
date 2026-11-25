---
id: m5-14
title: Service ClusterIP
domain: 5
level: examen
context: ckad-a
namespace: m5-14
time: 8
doc: https://kubernetes.io/docs/concepts/services-networking/service/
skill: services
weight: 7
---
Dans le namespace `m5-14`, expose le Deployment `ranking` (port conteneur 5678) par un Service
`ClusterIP` nommé `ranking-svc` : port `8080`.
