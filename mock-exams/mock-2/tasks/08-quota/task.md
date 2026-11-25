---
id: m2-08
title: ResourceQuota
domain: 4
level: examen
context: ckad-a
namespace: m2-08
time: 11
doc: https://kubernetes.io/docs/concepts/policy/resource-quotas/
skill: resources
weight: 12
---
Dans le namespace `m2-08`, crée la ResourceQuota `team-quota` : `4` Pods au plus,
`requests.cpu=800m`, `requests.memory=512Mi`. Puis crée le Pod `probe`
(`nginx:1.27-alpine`) avec requests `100m` / `64Mi` : il doit être accepté.
