---
id: d4-01
title: ConfigMap as environment variables
---
In namespace `d4-01`:

1. Create ConfigMap `app-config` with `APP_MODE=prod` and `APP_COLOR=blue`.
2. Create Pod `app` (image `busybox:1.37`, command `sh -c 'sleep 3600'`) receiving **all** keys of
   that ConfigMap as environment variables.
