---
id: d4-09
title: Type examen : application configurée
domain: 4
level: examen
context: ckad-a
namespace: d4-09
time: 9
doc: https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/
skill: configmaps
---
*Tâche type examen — 9 minutes.* Contexte `ckad-a`, namespace `d4-09`.

1. ConfigMap `portal-html` avec la clé `index.html` = `Portal OK`.
2. Secret `portal-key` avec la clé `API_KEY` = `k-7731`.
3. ServiceAccount `portal-sa`.
4. Deployment `portal`, 2 réplicas, image `nginx:1.27-alpine`, ServiceAccount `portal-sa` :
   - la ConfigMap montée en volume sur `/usr/share/nginx/html`
   - la variable `API_KEY` lue dans le Secret
   - requests `50m` CPU et `32Mi` mémoire
