---
id: d1-06
title: PersistentVolumeClaim et données persistantes
domain: 1
level: intermediaire
context: ckad-a
namespace: d1-06
time: 7
doc: https://kubernetes.io/docs/concepts/storage/persistent-volumes/
skill: volumes
---
Dans le namespace `d1-06` :

1. Crée un PersistentVolumeClaim `data` de `100Mi`, mode d'accès `ReadWriteOnce`,
   StorageClass `standard`.
2. Crée un Pod `writer` (image `busybox:1.37`) qui monte ce PVC sur `/data` et exécute
   `sh -c 'echo persistant > /data/proof.txt && sleep 3600'`.

Le PVC doit être `Bound` et le fichier `/data/proof.txt` doit exister dans le Pod.
