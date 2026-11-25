---
id: d1-09
title: Type examen : Pod de rapport
domain: 1
level: examen
context: ckad-a
namespace: d1-09
time: 8
doc: https://kubernetes.io/docs/concepts/storage/volumes/#emptydir
skill: multi-container
---
*Tâche type examen — 8 minutes.* Contexte `ckad-a`, namespace `d1-09`.

Crée un Pod `report` :

- volume `emptyDir` nommé `work`, **en mémoire** (`medium: Memory`), limité à `16Mi`
- init container `stamp` (`busybox:1.37`) qui écrit `rapport du jour` dans `/work/report.txt`
- conteneur `reader` (`busybox:1.37`) qui exécute `sh -c 'cat /work/report.txt && sleep 3600'`
- les deux conteneurs montent `work` sur `/work`

Enregistre le manifeste utilisé dans `~/ckad/d1-09/report.yaml`.
