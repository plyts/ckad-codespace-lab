---
id: d1-03
title: Backup CronJob
---
In namespace `d1-03`, create a CronJob named `backup`:

- runs **every 5 minutes**
- image `busybox:1.37`, command `sh -c 'echo sauvegarde'`
- keeps **2** successful Jobs and **1** failed Job in the history
- a new run must **never** start while the previous one is still running
