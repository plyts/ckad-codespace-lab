---
id: m1-05
title: Non-root Pod
---
In namespace `m1-05`, create Pod `hardened` (`busybox:1.37`, `sh -c 'sleep 3600'`) running as user
`2000`, **refusing to start as root** (`runAsNonRoot`), forbidding privilege escalation and adding
**only** the `NET_BIND_SERVICE` capability after dropping all the others.
