---
id: m5-07
title: CrashLoopBackOff
---
In namespace `m5-07`, Deployment `notifier` is in `CrashLoopBackOff`. Read its command: it waits for a
file. Fix the Deployment **without changing its command**: mount a ConfigMap `notifier-config` (key
`ready`, value `yes`) on `/config`.
