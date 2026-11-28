---
id: m2-09
title: Two-path Ingress
---
In namespace `m2-09`, create Ingress `home-ing` (class `traefik`) for host `m2.lab.local`: `/` to Service `home`
(port 80) and `/docs` to Service `docs` (port 9090), as `pathType: Prefix`.
