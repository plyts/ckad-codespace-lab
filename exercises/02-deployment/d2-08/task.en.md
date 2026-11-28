---
id: d2-08
title: 20% canary
---
In namespace `d2-08`, Service `api` sends traffic to the 5 Pods of `api-v1` (labels `app=api`,
`track=stable`).

Set up a **canary**: about **20%** of the requests must reach a new version, without changing the
Service:

- Deployment `api-v2`, image `hashicorp/http-echo:1.0.0`, argument `-text=api v2`, port 5678,
  labels `app=api` and `track=canary`
- **5 Pods** in total behind the Service: 4 stable and 1 canary
