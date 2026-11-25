---
id: d4-06
title: SecurityContext durci
domain: 4
level: intermediaire
context: ckad-a
namespace: d4-06
time: 6
doc: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
skill: securitycontext
---
Dans le namespace `d4-06`, crée le Pod `secure` (image `busybox:1.37`,
`sh -c 'sleep 3600'`) :

- au niveau du **Pod** : utilisateur `1000`, groupe `3000`, `fsGroup` `2000`
- au niveau du **conteneur** : pas d'escalade de privilèges, système de fichiers racine
  en **lecture seule**, **toutes** les capabilities retirées
