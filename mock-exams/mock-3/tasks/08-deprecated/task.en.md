---
id: m3-08
title: Ingress on a removed API
---
`~/ckad/m3-08/ingress.yaml` uses a removed API. Convert **the file** to `networking.k8s.io/v1`
(pathType `Prefix`), then apply it: `legacy.m3.lab.local` must answer `web ok`.
