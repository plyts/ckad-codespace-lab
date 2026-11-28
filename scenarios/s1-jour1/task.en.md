---
id: s1-jour1
title: Shop, day 1: deploy v1
---
**Running scenario, day 1.** Context `ckad-a`, namespace `boutique-j1`.
Deploy v1 of the shop (diagram in `app/boutique/README.md`):

| Component | Deployment | Image and arguments | Replicas | Service |
|---|---|---|---|---|
| data | `redis` | `redis:7.4-alpine` | 1 | `redis`, port 6379 |
| API | `api` | `hashicorp/http-echo:1.0.0`, argument `-text=api v1` (listens on 5678) | 2 | `api`, port **80** to 5678 |
| web | `front` | `nginx:1.27-alpine` | 2 | `front`, port 80 |

Every Deployment carries the label `app=<name>`. Check from a Pod that `http://api` answers `api v1`.
