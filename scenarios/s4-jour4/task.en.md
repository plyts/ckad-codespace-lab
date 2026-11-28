---
id: s4-jour4
title: Shop, day 4: network isolation and Ingress
---
**Running scenario, day 4.** Context `ckad-a`, namespace `boutique-j4`.

1. NetworkPolicy `default-deny`: all **incoming** traffic denied in the namespace.
2. NetworkPolicy `front-to-api`: Pods `app=front` may reach `app=api` (port 5678).
3. NetworkPolicy `api-to-redis`: Pods `app=api` may reach `app=redis` (port 6379).
4. NetworkPolicy `ingress-to-front`: namespace `traefik` may reach `app=front` (port 80).
5. Ingress `boutique` (class `traefik`), host `boutique.lab.local`, `/` to `front:80`.

The front must **not** be able to reach Redis directly; the API must.
