---
id: m5-09
title: Removed API
---
`~/ckad/m5-09/ingress.yaml` uses a removed API. Convert **the file** to `networking.k8s.io/v1`
(pathType `Prefix`), then apply it: `old.m5.lab.local` must answer `web ok`.
