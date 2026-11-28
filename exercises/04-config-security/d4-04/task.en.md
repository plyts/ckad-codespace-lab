---
id: d4-04
title: Requests and limits
---
In namespace `d4-04`, create Pod `bounded` (image `nginx:1.27-alpine`) with:

- requests: `100m` CPU and `64Mi` memory
- limits: `200m` CPU and `128Mi` memory

Write its **QoS class** into `~/ckad/d4-04/qos.txt`.
