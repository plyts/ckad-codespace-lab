---
id: d5-01
title: Exposer un Deployment (ClusterIP)
domain: 5
level: debutant
context: ckad-a
namespace: d5-01
time: 3
doc: https://kubernetes.io/docs/concepts/services-networking/service/
skill: services
---
Dans le namespace `d5-01`, expose le Deployment `web` par un Service **ClusterIP**
nommé `web`, port `80` vers le port `80` des conteneurs.
