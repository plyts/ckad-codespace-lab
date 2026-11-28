---
id: d5-05
title: Ingress with two paths
---
In namespace `d5-05`, Services `front` (port 80) and `api` (port 8080) exist.

Create Ingress `shop` (class `traefik`) for host `shop.lab.local`:

- path `/` (Prefix) to `front:80`
- path `/api` (Prefix) to `api:8080`

Test: `curl -H 'Host: shop.lab.local' http://localhost:8080/api` in the Codespace.
