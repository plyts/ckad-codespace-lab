---
id: m5-16
title: Ingress
---
In namespace `m5-16`, create Ingress `front-ing` (class `traefik`) for host `m5.lab.local`: `/` to Service `front`
(port 80) and `/api` to Service `api` (port 9090), as `pathType: Prefix`.
