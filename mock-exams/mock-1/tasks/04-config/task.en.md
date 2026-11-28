---
id: m1-04
title: ConfigMap and Secret as variables
---
In namespace `m1-04`: ConfigMap `worker-cfg` (`LEVEL=debug`) and Secret `worker-sec` (`TOKEN=t0k3n-a1`).
Pod `worker` (`busybox:1.37`, `sh -c 'sleep 3600'`) receiving variable `LOG_LEVEL` from `worker-cfg` (key
`LEVEL`) and `API_TOKEN` from `worker-sec` (key `TOKEN`).
