---
id: m4-02
title: DaemonSet on every node
---
In namespace `m4-02`, create DaemonSet `log-agent` (`busybox:1.37`, `sh -c 'sleep 3600'`) placing a Pod
on **every** node of the cluster, control plane included.
