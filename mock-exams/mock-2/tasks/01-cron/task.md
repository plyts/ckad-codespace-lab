---
id: m2-01
title: CronJob et exécution manuelle
domain: 1
level: examen
context: ckad-a
namespace: m2-01
time: 9
doc: https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/
skill: workloads
weight: 10
---
Dans le namespace `m2-01`, crée le CronJob `report` : planification `30 1 * * *`, image
`busybox:1.37`, commande `sh -c 'date'`, `concurrencyPolicy: Replace`, **5** Jobs
réussis conservés. Puis déclenche **tout de suite** une exécution manuelle sous la forme
d'un Job nommé `report-manual`.
