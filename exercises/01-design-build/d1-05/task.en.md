---
id: d1-05
title: Init container preparing content
---
In namespace `d1-05`, create a Pod `site` (label `app=site`):

- an init container `prepare`, image `busybox:1.37`, writing `site prêt` into `/work/index.html`
- a container `nginx`, image `nginx:1.27-alpine`, serving that file: the same `emptyDir` volume is
  mounted on `/usr/share/nginx/html`

An HTTP request on port 80 of the Pod must return `site prêt`.
