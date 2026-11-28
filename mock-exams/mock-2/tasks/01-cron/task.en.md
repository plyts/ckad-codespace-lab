---
id: m2-01
title: CronJob and manual run
---
In namespace `m2-01`, create CronJob `report`: schedule `30 1 * * *`, image `busybox:1.37`, command
`sh -c 'date'`, `concurrencyPolicy: Replace`, **5** successful Jobs kept. Then trigger a manual
run **right now** as a Job named `report-manual`.
