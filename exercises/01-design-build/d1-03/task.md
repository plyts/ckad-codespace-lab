---
id: d1-03
title: CronJob de sauvegarde
domain: 1
level: debutant
context: ckad-a
namespace: d1-03
time: 4
doc: https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
skill: workloads
---
Dans le namespace `d1-03`, crée un CronJob nommé `backup` :

- exécution **toutes les 5 minutes**
- image `busybox:1.37`, commande `sh -c 'echo sauvegarde'`
- garde **2** Jobs réussis et **1** Job échoué dans l'historique
- une nouvelle exécution ne doit **jamais** démarrer si la précédente tourne encore
