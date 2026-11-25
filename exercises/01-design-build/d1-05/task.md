---
id: d1-05
title: Init container qui prépare le contenu
domain: 1
level: intermediaire
context: ckad-a
namespace: d1-05
time: 6
doc: https://kubernetes.io/docs/concepts/workloads/pods/init-containers/
skill: multi-container
---
Dans le namespace `d1-05`, crée un Pod `site` (label `app=site`) :

- un init container `prepare`, image `busybox:1.37`, qui écrit `site prêt` dans
  `/work/index.html`
- un conteneur `nginx`, image `nginx:1.27-alpine`, qui sert ce fichier : le même volume
  `emptyDir` est monté sur `/usr/share/nginx/html`

Une requête HTTP sur le port 80 du Pod doit renvoyer `site prêt`.
