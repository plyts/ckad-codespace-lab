---
id: d3-06
title: Pod Pending : lire les événements
domain: 3
level: intermediaire
context: ckad-a
namespace: d3-06
time: 5
doc: https://kubernetes.io/docs/tasks/debug/debug-application/debug-pods/
skill: debugging
---
Dans le namespace `d3-06`, le Pod `big` reste `Pending`.

1. Écris dans `~/ckad/d3-06/reason.txt` la **raison** (champ `Reason`) de l'événement
   qui l'explique.
2. Fais tourner le Pod `big` (même nom, même image) en demandant `50m` de CPU.
