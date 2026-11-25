---
id: d5-06
title: NetworkPolicy : deny puis autoriser
domain: 5
level: intermediaire
context: ckad-a
namespace: d5-06
time: 7
doc: https://kubernetes.io/docs/concepts/services-networking/network-policies/
skill: networkpolicy
---
Dans le namespace `d5-06`, le Service `api` (Pods `app=api`, port 80) est ouvert à tous.

1. NetworkPolicy `default-deny` : **bloque tout le trafic entrant** vers tous les Pods
   du namespace.
2. NetworkPolicy `allow-frontend` : autorise l'entrée vers les Pods `app=api` sur le
   port `80`, **uniquement** depuis les Pods du namespace étiquetés `role=frontend`.
