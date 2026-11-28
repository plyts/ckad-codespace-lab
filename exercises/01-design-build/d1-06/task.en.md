---
id: d1-06
title: PersistentVolumeClaim and persistent data
---
In namespace `d1-06`:

1. Create a PersistentVolumeClaim `data` of `100Mi`, access mode `ReadWriteOnce`, StorageClass
   `standard`.
2. Create a Pod `writer` (image `busybox:1.37`) mounting this PVC on `/data` and running
   `sh -c 'echo persistant > /data/proof.txt && sleep 3600'`.

The PVC must be `Bound` and the file `/data/proof.txt` must exist in the Pod.
