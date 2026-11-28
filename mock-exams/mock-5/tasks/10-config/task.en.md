---
id: m5-10
title: ConfigMap and Secret
---
In namespace `m5-10`: ConfigMap `agent-cfg` (`LEVEL=warn`) and Secret `agent-sec` (`TOKEN=s3cr3t-b2`).
Pod `agent` (`busybox:1.37`, `sh -c 'sleep 3600'`) receiving variable `LOG_LEVEL` from `agent-cfg` (key
`LEVEL`) and `API_TOKEN` from `agent-sec` (key `TOKEN`).
