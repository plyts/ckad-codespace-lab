---
id: d4-06
title: Hardened SecurityContext
---
In namespace `d4-06`, create Pod `secure` (image `busybox:1.37`, `sh -c 'sleep 3600'`):

- at **Pod** level: user `1000`, group `3000`, `fsGroup` `2000`
- at **container** level: no privilege escalation, **read-only** root filesystem, **all**
  capabilities dropped
