---
id: m4-12
title: SecurityContext
domain: 4
level: examen
context: ckad-b
namespace: m4-12
time: 7
doc: https://kubernetes.io/docs/tasks/configure-pod-container/security-context/
skill: securitycontext
weight: 6
---
Dans le namespace `m4-12`, crée le Pod `runner` (`busybox:1.37`, `sh -c 'sleep 3600'`) qui
s'exécute en utilisateur `1500`, **refuse de démarrer en root** (`runAsNonRoot`), interdit
l'escalade de privilèges et ajoute **seulement** la capability `NET_BIND_SERVICE` après avoir
retiré toutes les autres.
