---
id: s2-jour2
title: Shop, day 2: configuration and scaling
---
**Running scenario, day 2.** Context `ckad-a`, namespace `boutique-j2` (v1 runs there).

1. ConfigMap `front-html`, key `index.html` = `Boutique jour 2`, mounted in `front` on
   `/usr/share/nginx/html`.
2. Secret `redis-auth`, key `password` = `r3d1s-pass`; the API receives variable `REDIS_PASSWORD`
   from that Secret.
3. Container `api`: requests `50m` / `32Mi`, limits `100m` / `64Mi`.
4. Scale the API to **3 replicas**.
