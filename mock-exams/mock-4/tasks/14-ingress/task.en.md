---
id: m4-14
title: Ingress
---
In namespace `m4-14`, create Ingress `shop-ing` (class `traefik`) for host `m4.lab.local`: `/` to Service `shop`
(port 80) and `/cart` to Service `cart` (port 9090), as `pathType: Prefix`.
