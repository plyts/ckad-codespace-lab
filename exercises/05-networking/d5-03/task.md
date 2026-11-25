---
id: d5-03
title: DNS des Services
domain: 5
level: debutant
context: ckad-a
namespace: d5-03
time: 4
doc: https://kubernetes.io/docs/concepts/services-networking/dns-pod-service/
skill: services
---
Dans le namespace `d5-03`, un Service `db` existe.

1. Écris son **nom DNS complet** (FQDN) dans `~/ckad/d5-03/fqdn.txt`.
2. Écris son adresse **ClusterIP** dans `~/ckad/d5-03/ip.txt`.
3. Vérifie la résolution depuis un Pod jetable (`busybox:1.37`, `nslookup`).
