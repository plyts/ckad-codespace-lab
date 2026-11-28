---
id: d5-09
title: Exam-style: publish a protected API
---
*Exam-style task — 9 minutes.* Context `ckad-a`, namespace `d5-09`.

Deployment `catalog` (container port 5678) is not exposed.

1. ClusterIP Service `catalog`, port `8080` to `5678`.
2. Ingress `catalog` (class `traefik`), host `catalog.lab.local`, path `/catalog` (Prefix) to that
   Service.
3. NetworkPolicy `catalog-from-ingress`: Pods `app=catalog` accept incoming traffic **only** from
   namespace `traefik`, port 5678.
