---
id: m4-13
title: Quota
domain: 4
level: examen
context: ckad-a
namespace: m4-13
time: 7
doc: https://kubernetes.io/docs/concepts/policy/resource-quotas/
skill: resources
weight: 6
---
Dans le namespace `m4-13`, crée la ResourceQuota `team-quota` : `6` Pods au plus,
`requests.cpu=1`, `requests.memory=1Gi`. Puis crée le Pod `probe`
(`nginx:1.27-alpine`) avec requests `100m` / `64Mi` : il doit être accepté.
