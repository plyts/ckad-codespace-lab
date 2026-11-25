---
id: d4-05
title: ResourceQuota et LimitRange
domain: 4
level: intermediaire
context: ckad-a
namespace: d4-05
time: 6
doc: https://kubernetes.io/docs/concepts/policy/resource-quotas/
skill: resources
---
Dans le namespace `d4-05` :

1. Crée la ResourceQuota `ns-quota` : au plus `5` Pods, `requests.cpu=1`,
   `requests.memory=1Gi`, `limits.cpu=2`, `limits.memory=2Gi`.
2. Crée la LimitRange `defaults` qui donne aux conteneurs sans ressources :
   requests `50m` / `32Mi` et limits `100m` / `64Mi`.
3. Vérifie-le : crée le Pod `plain` (`nginx:1.27-alpine`) **sans** section `resources`.
