---
id: d1-08
title: DaemonSet on every node
---
In namespace `d1-08`, create a DaemonSet `node-agent` (label `app=node-agent`), image
`busybox:1.37`, command `sh -c 'sleep 3600'`.

A Pod must run on **every** node of the cluster, **control plane included**.
