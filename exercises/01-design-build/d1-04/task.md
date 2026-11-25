---
id: d1-04
title: Sidecar qui suit un journal
domain: 1
level: intermediaire
context: ckad-a
namespace: d1-04
time: 7
doc: https://kubernetes.io/docs/concepts/workloads/pods/sidecar-containers/
skill: multi-container
---
Dans le namespace `d1-04`, crée un Pod `logger` avec deux conteneurs qui partagent un volume
`emptyDir` nommé `logs`, monté sur `/var/log/app` :

- conteneur principal `app`, image `busybox:1.37`, qui écrit une ligne toutes les 2 secondes :
  `sh -c 'while true; do echo "tick $(date)" >> /var/log/app/app.log; sleep 2; done'`
- conteneur sidecar `shipper`, image `busybox:1.37`, qui affiche ce fichier en continu :
  `sh -c 'tail -F /var/log/app/app.log'`

Utilise un **sidecar natif** (conteneur d'init redémarré en continu).
`kubectl logs logger -c shipper` doit afficher les lignes `tick`.
