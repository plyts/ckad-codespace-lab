---
id: d3-02
title: Liveness probe HTTP
domain: 3
level: debutant
context: ckad-a
namespace: d3-02
time: 4
doc: https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/
skill: probes
---
Dans le namespace `d3-02`, crée un Pod `web` (image `nginx:1.27-alpine`) avec une
**liveness probe** HTTP `GET /` sur le port `80`, qui commence après **5 secondes** et
s'exécute toutes les **10 secondes**.
