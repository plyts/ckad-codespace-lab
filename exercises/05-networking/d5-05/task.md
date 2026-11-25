---
id: d5-05
title: Ingress à deux chemins
domain: 5
level: intermediaire
context: ckad-a
namespace: d5-05
time: 7
doc: https://kubernetes.io/docs/concepts/services-networking/ingress/
skill: ingress
---
Dans le namespace `d5-05`, les Services `front` (port 80) et `api` (port 8080) existent.

Crée l'Ingress `shop` (classe `traefik`) pour l'hôte `shop.lab.local` :

- le chemin `/` (Prefix) vers `front:80`
- le chemin `/api` (Prefix) vers `api:8080`

Test : `curl -H 'Host: shop.lab.local' http://localhost:8080/api` dans le Codespace.
