---
id: m4-11
title: RBAC
domain: 4
level: examen
context: ckad-a
namespace: m4-11
time: 7
doc: https://kubernetes.io/docs/reference/access-authn-authz/rbac/
skill: rbac
weight: 6
---
Dans le namespace `m4-11`, crée le ServiceAccount `deployer`, le Role `deployer-role`
(verbes `get,list,create,update` sur `deployments`) et le RoleBinding `deployer-binding` qui les relie.
