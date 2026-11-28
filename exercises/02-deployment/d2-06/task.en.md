---
id: d2-06
title: Install a Helm chart
---
A Helm chart is available in `~/ckad/d2-06/webapp`.

1. Install it in namespace `d2-06` as release `shop`, with `replicaCount=2` and
   `image.tag=1.28-alpine`.
2. Write the chart's **default** values (output of `helm show values`) into
   `~/ckad/d2-06/values.txt`.
