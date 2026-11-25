---
id: m5-03
title: Init container
domain: 1
level: examen
context: ckad-a
namespace: m5-03
time: 7
doc: https://kubernetes.io/docs/concepts/workloads/pods/init-containers/
skill: multi-container
weight: 6
---
Dans le namespace `m5-03`, crée le Pod `status` : un init container `seed` (`busybox:1.37`)
écrit `tout va bien` dans `/seed/index.html` ; le conteneur `web` (`nginx:1.27-alpine`) sert ce
fichier (même volume `emptyDir` monté sur `/usr/share/nginx/html`).
