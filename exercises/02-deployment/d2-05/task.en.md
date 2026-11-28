---
id: d2-05
title: Tuning the deployment strategy
---
In namespace `d2-05`, change Deployment `api`:

- a rolling update that **never** removes a Pod before a new one is ready (`maxUnavailable: 0`)
  and creates **at most 1** extra Pod (`maxSurge: 1`)
- a Pod only counts as available after being ready for **5 seconds**
- keep **4** old ReplicaSets at most
