---
id: d4-01
title: ConfigMap en variables d'environnement
domain: 4
level: debutant
context: ckad-a
namespace: d4-01
time: 4
doc: https://kubernetes.io/docs/tasks/configure-pod-container/configure-pod-configmap/
skill: configmaps
---
Dans le namespace `d4-01` :

1. Crée la ConfigMap `app-config` avec `APP_MODE=prod` et `APP_COLOR=blue`.
2. Crée le Pod `app` (image `busybox:1.37`, commande `sh -c 'sleep 3600'`) qui reçoit
   **toutes** les clés de cette ConfigMap comme variables d'environnement.
