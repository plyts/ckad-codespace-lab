---
id: m5-02
title: PVC
---
In namespace `m5-02`: PVC `media-pvc` of `150Mi` (`ReadWriteOnce`, StorageClass `standard`), then Pod
`media` (`busybox:1.37`) mounting it on `/media` and running
`sh -c 'echo photo > /media/data.txt && sleep 3600'`.
