---
id: m3-02
title: Init container
domain: 1
level: examen
context: ckad-b
namespace: m3-02
time: 8
doc: https://kubernetes.io/docs/concepts/workloads/pods/init-containers/
skill: multi-container
weight: 7
---
Dans le namespace `m3-02`, crée le Pod `landing` : un init container `seed` (`busybox:1.37`)
écrit `bienvenue m3` dans `/seed/index.html` ; le conteneur `web` (`nginx:1.27-alpine`) sert ce
fichier (même volume `emptyDir` monté sur `/usr/share/nginx/html`).
