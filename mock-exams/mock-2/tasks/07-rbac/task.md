---
id: m2-07
title: Droits d'un ServiceAccount
domain: 4
level: examen
context: ckad-b
namespace: m2-07
time: 12
doc: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
skill: rbac
weight: 13
---
Dans le namespace `m2-07`, crée le ServiceAccount `auditor`, le Role `auditor-role`
(verbes `get,list,watch` sur `deployments,pods`) et le RoleBinding `auditor-binding` qui les relie.
