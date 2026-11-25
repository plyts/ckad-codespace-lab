---
id: d3-09
title: Type examen : sondes mal réglées
domain: 3
level: examen
context: ckad-a
namespace: d3-09
time: 8
doc: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
skill: probes
---
*Tâche type examen — 8 minutes.* Contexte `ckad-a`, namespace `d3-09`.

Les Pods du Deployment `orders` redémarrent sans cesse.

1. Écris dans `~/ckad/d3-09/cause.txt` le message d'événement qui explique les
   redémarrages (une ligne suffit).
2. Corrige la **liveness probe** pour qu'elle vise le bon port de l'application.
3. Ajoute une **startup probe** HTTP `GET /` sur ce même port, `failureThreshold: 10`,
   `periodSeconds: 2`.
