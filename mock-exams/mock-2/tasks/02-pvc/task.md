---
id: m2-02
title: Stockage persistant
domain: 1
level: examen
context: ckad-a
namespace: m2-02
time: 9
doc: https://kubernetes.io/docs/concepts/storage/persistent-volumes/
skill: volumes
weight: 10
---
Dans le namespace `m2-02` : PVC `cache-pvc` de `200Mi` (`ReadWriteOnce`, StorageClass
`standard`), puis Pod `cache` (`busybox:1.37`) qui le monte sur `/cache` et exécute
`sh -c 'echo chaud > /cache/data.txt && sleep 3600'`.
