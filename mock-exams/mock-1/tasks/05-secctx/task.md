---
id: m1-05
title: Pod non root
domain: 4
level: examen
context: ckad-a
namespace: m1-05
time: 7
doc: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
skill: securitycontext
weight: 12
---
Dans le namespace `m1-05`, crée le Pod `hardened` (`busybox:1.37`, `sh -c 'sleep 3600'`) qui
s'exécute en utilisateur `2000`, **refuse de démarrer en root** (`runAsNonRoot`), interdit
l'escalade de privilèges et ajoute **seulement** la capability `NET_BIND_SERVICE` après avoir
retiré toutes les autres.
