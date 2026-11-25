---
id: d2-06
title: Installer un chart Helm
domain: 2
level: intermediaire
context: ckad-a
namespace: d2-06
time: 6
doc: https://helm.sh/docs/helm/helm_install/
skill: helm
---
Un chart Helm est disponible dans `~/ckad/d2-06/webapp`.

1. Installe-le dans le namespace `d2-06` sous le nom de release `shop`, avec
   `replicaCount=2` et `image.tag=1.28-alpine`.
2. Écris dans `~/ckad/d2-06/values.txt` les valeurs **par défaut** du chart
   (sortie de `helm show values`).
