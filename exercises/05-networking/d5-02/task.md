---
id: d5-02
title: Service NodePort
domain: 5
level: debutant
context: ckad-a
namespace: d5-02
time: 4
doc: https://kubernetes.io/docs/concepts/services-networking/service/#type-nodeport
skill: services
---
Dans le namespace `d5-02`, crée un Service **NodePort** `web-np` qui expose le
Deployment `web` : port `80`, port cible `80`, **nodePort `30080`**.
