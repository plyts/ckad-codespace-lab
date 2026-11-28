---
id: m5-04
title: Kustomize
---
Kustomize base: `~/ckad/m5-04/base`. Create the overlay `~/ckad/m5-04/overlay` that deploys into
`m5-04`, prefixes names with `prd-`, sets **3 replicas**, adds the label `tier=prod`,
and replaces the image with `nginx:1.28-alpine`. Apply it.
