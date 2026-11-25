---
id: d4-04
title: Requests et limits
domain: 4
level: intermediaire
context: ckad-a
namespace: d4-04
time: 4
doc: https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/
skill: resources
---
Dans le namespace `d4-04`, crée le Pod `bounded` (image `nginx:1.27-alpine`) avec :

- requests : `100m` de CPU et `64Mi` de mémoire
- limits : `200m` de CPU et `128Mi` de mémoire

Écris sa **classe QoS** dans `~/ckad/d4-04/qos.txt`.
