---
id: d5-09
title: Type examen : publier une API protégée
domain: 5
level: examen
context: ckad-a
namespace: d5-09
time: 9
doc: https://kubernetes.io/docs/concepts/services-networking/ingress/
skill: ingress
---
*Tâche type examen — 9 minutes.* Contexte `ckad-a`, namespace `d5-09`.

Le Deployment `catalog` (port conteneur 5678) n'est pas exposé.

1. Service ClusterIP `catalog`, port `8080` vers `5678`.
2. Ingress `catalog` (classe `traefik`), hôte `catalog.lab.local`, chemin `/catalog`
   (Prefix) vers ce Service.
3. NetworkPolicy `catalog-from-ingress` : les Pods `app=catalog` n'acceptent du trafic
   entrant **que** depuis le namespace `traefik`, port 5678.
