---
id: d2-09
title: Exam-style: Kustomize overlay
---
*Exam-style task — 8 minutes.* Context `ckad-a`.

A Kustomize base is provided in `~/ckad/d2-09/base`. Create the overlay
`~/ckad/d2-09/overlays/prod/kustomization.yaml` that:

- uses the base
- deploys into namespace `d2-09`
- prefixes names with `prod-`
- sets the Deployment to **3 replicas**
- adds the label `env=prod` to every resource

Apply the overlay with `kubectl`.
