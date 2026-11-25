---
id: d3-08
title: kubectl top : le Pod le plus gourmand
domain: 3
level: avance
context: ckad-a
namespace: d3-08
time: 5
doc: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_top/
skill: monitoring
requires: metrics-server
---
Dans le namespace `d3-08`, trois Pods `worker-*` tournent. L'un consomme beaucoup de CPU.
Écris son **nom** dans `~/ckad/d3-08/top.txt`.

(Il faut metrics-server : attends une minute après le démarrage pour avoir des mesures.)
