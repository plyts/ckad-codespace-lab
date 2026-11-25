---
id: s4-jour4
title: Boutique, journée 4 : isolation réseau et Ingress
domain: 0
level: avance
context: ckad-a
namespace: boutique-j4
time: 15
doc: https://kubernetes.io/docs/concepts/services-networking/network-policies/
skill: fil-conducteur
---
**Fil conducteur, journée 4.** Contexte `ckad-a`, namespace `boutique-j4`.

1. NetworkPolicy `default-deny` : tout trafic **entrant** refusé dans le namespace.
2. NetworkPolicy `front-to-api` : les Pods `app=front` peuvent joindre `app=api` (port 5678).
3. NetworkPolicy `api-to-redis` : les Pods `app=api` peuvent joindre `app=redis` (port 6379).
4. NetworkPolicy `ingress-to-front` : le namespace `traefik` peut joindre `app=front` (port 80).
5. Ingress `boutique` (classe `traefik`), hôte `boutique.lab.local`, `/` vers `front:80`.

Le front ne doit **pas** pouvoir joindre Redis directement.
