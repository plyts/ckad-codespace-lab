---
id: m3-04
title: Kustomize overlay
---
Kustomize base: `~/ckad/m3-04/base`. Create the overlay `~/ckad/m3-04/overlay` that deploys into
`m3-04`, prefixes names with `stg-`, sets **2 replicas**, adds the label `tier=staging`,
and replaces the image with `nginx:1.28-alpine`. Apply it.
