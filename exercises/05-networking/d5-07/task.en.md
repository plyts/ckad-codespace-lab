---
id: d5-07
title: Egress NetworkPolicy
---
In namespace `d5-07`, create NetworkPolicy `client-egress` applying to Pods `app=client` and letting
them out **only** to:

- Pods `app=db` of namespace `d5-07-db`, TCP port `80`
- the cluster DNS (port `53`, UDP and TCP)

Any other outgoing traffic from those Pods (for example to `web.d5-07`) must be blocked.
