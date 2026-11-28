---
id: m4-12
title: SecurityContext
---
In namespace `m4-12`, create Pod `runner` (`busybox:1.37`, `sh -c 'sleep 3600'`) running as user
`1500`, **refusing to start as root** (`runAsNonRoot`), forbidding privilege escalation and adding
**only** the `NET_BIND_SERVICE` capability after dropping all the others.
