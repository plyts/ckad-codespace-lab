---
id: s2-jour2
title: Boutique, journée 2 : configuration et montée en charge
domain: 0
level: intermediaire
context: ckad-a
namespace: boutique-j2
time: 15
doc: https://kubernetes.io/docs/concepts/configuration/configmap/
skill: fil-conducteur
---
**Fil conducteur, journée 2.** Contexte `ckad-a`, namespace `boutique-j2` (la v1 y tourne).

1. ConfigMap `front-html`, clé `index.html` = `Boutique jour 2`, montée dans `front` sur
   `/usr/share/nginx/html`.
2. Secret `redis-auth`, clé `password` = `r3d1s-pass` ; l'API reçoit la variable
   `REDIS_PASSWORD` depuis ce Secret.
3. Conteneur `api` : requests `50m` / `32Mi`, limits `100m` / `64Mi`.
4. Monte l'API à **3 réplicas**.
