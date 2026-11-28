---
id: m3-06
title: Recreate strategy
---
In namespace `m3-06`, configure Deployment `legacy` so that every update **stops all old Pods before**
creating the new ones (`Recreate` strategy). Then update it to `nginx:1.28-alpine`.
