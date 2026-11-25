---
id: d2-07
title: Bascule blue/green
domain: 2
level: avance
context: ckad-a
namespace: d2-07
time: 7
doc: https://kubernetes.io/docs/concepts/services-networking/service/
skill: strategies
---
Dans le namespace `d2-07`, la version **blue** de l'application tourne (Deployment
`web-blue`) et le Service `web` lui envoie le trafic.

1. Déploie la version **green** : Deployment `web-green`, 2 réplicas, image
   `hashicorp/http-echo:1.0.0` avec l'argument `-text=green`, port 5678, labels
   `app=web` et `version=green`.
2. Quand green est prête, **bascule tout le trafic** du Service `web` vers green.
3. Garde `web-blue` en place (retour arrière possible).
