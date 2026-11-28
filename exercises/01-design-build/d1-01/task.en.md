---
id: d1-01
title: First nginx Pod
---
In namespace `d1-01`, create a Pod named `web`:

- image `nginx:1.27-alpine`
- label `app=web`
- container port `80`

The Pod must be `Running` and ready.
