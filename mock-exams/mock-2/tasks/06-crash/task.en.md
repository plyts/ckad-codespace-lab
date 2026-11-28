---
id: m2-06
title: CrashLoopBackOff: missing file
---
In namespace `m2-06`, Deployment `billing` is in `CrashLoopBackOff`. Read its command: it waits for a
file. Fix the Deployment **without changing its command**: mount a ConfigMap `billing-config` (key
`ready`, value `yes`) on `/config`.
