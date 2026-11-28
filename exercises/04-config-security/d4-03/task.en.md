---
id: d4-03
title: Dedicated ServiceAccount
---
In namespace `d4-03`, create ServiceAccount `deployer`, then Pod `tool` (image `busybox:1.37`,
`sh -c 'sleep 3600'`) using it. The ServiceAccount token must **not** be mounted automatically in
that Pod.
