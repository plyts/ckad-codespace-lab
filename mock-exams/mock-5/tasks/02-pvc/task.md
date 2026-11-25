---
id: m5-02
title: PVC
domain: 1
level: examen
context: ckad-a
namespace: m5-02
time: 8
doc: https://kubernetes.io/docs/concepts/storage/persistent-volumes/
skill: volumes
weight: 7
---
Dans le namespace `m5-02` : PVC `media-pvc` de `150Mi` (`ReadWriteOnce`, StorageClass
`standard`), puis Pod `media` (`busybox:1.37`) qui le monte sur `/media` et exécute
`sh -c 'echo photo > /media/data.txt && sleep 3600'`.
