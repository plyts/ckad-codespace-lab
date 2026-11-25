---
id: d5-08
title: Ingress en panne
domain: 5
level: avance
context: ckad-a
namespace: d5-08
time: 6
doc: https://kubernetes.io/docs/concepts/services-networking/ingress/
skill: ingress
---
Dans le namespace `d5-08`, l'Ingress `blog` ne sert rien : une requête sur l'hôte
`blog.lab.local` via le contrôleur Ingress du cluster doit renvoyer `blog ok`.
Trouve et corrige les erreurs **de l'Ingress**.
