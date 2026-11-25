---
id: m3-13
title: Service NodePort
domain: 5
level: examen
context: ckad-b
namespace: m3-13
time: 12
doc: https://kubernetes.io/docs/concepts/services-networking/service/
skill: services
weight: 10
---
Dans le namespace `m3-13`, expose le Deployment `gateway` (port conteneur 5678) par un Service
`NodePort` nommé `gateway-svc` : port `80`, nodePort `30180`.
