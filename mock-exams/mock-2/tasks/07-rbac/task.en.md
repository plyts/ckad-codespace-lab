---
id: m2-07
title: ServiceAccount permissions
---
In namespace `m2-07`, create ServiceAccount `auditor`, Role `auditor-role` (verbs `get,list,watch` on
`deployments,pods`) and RoleBinding `auditor-binding` tying them together.
