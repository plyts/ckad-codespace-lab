---
title: Running scenario
color: gris
---
# Running scenario: the shop over four days

A small, realistic application evolves day after day and goes through all five domains:

```text
 browser ──▶ Ingress (Traefik) ──▶ front (nginx :80)
                                     │
                                     ▼
                                   api (http-echo :5678, Service :80)
                                     │
                                     ▼
                                   redis (:6379)
```

| Day | What changes | Domains |
|---|---|---|
| 1 | Deploy v1: 3 Deployments, 3 Services | 1, 2, 5 |
| 2 | Mounted ConfigMap, Secret as env var, resources, 3 replicas | 4, 2 |
| 3 | Broken v2, real **CrashLoopBackOff**, diagnosis, rollback | 2, 3 |
| 4 | Layered NetworkPolicies, Ingress | 5 |
| failures | Three failures at once; a ServiceAccount hitting `Forbidden` | 3, 4, 5 |

Each day is **independent**: `ex scenario s3-jour3` first replays day 2's reference state
(`app/boutique/jour2.yaml`), then triggers the incident.

## Day 1 state, as it runs

{{capture:get-all}}

## The scenarios

{{scenarios}}

:::verif
After each day, `ex check <id>` checks the real state. Scenario 4 also checks that the front
**cannot** reach Redis: a throwaway `app=front` Pod tries a real TCP connection (Redis `PING`), which
must fail, while an `app=api` Pod must get `PONG`.
:::
