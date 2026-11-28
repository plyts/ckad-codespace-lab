---
id: m2-02
title: Persistent storage
---
In namespace `m2-02`: PVC `cache-pvc` of `200Mi` (`ReadWriteOnce`, StorageClass `standard`), then Pod
`cache` (`busybox:1.37`) mounting it on `/cache` and running
`sh -c 'echo chaud > /cache/data.txt && sleep 3600'`.
