---
id: s3-jour3
title: Shop, day 3: incident and rollback
---
**Running scenario, day 3.** Context `ckad-a`, namespace `boutique-j3`.

The team just deployed **v2** of the API. The new Pods do not start.

1. Write into `~/ckad/s3-jour3/incident.txt` the **status** shown by the new Pods (STATUS column of
   `kubectl get pods`) and, on a second line, the cause found in their logs.
2. Go back to the **v1 stable** revision.
3. The API must answer `api v1` with 3 ready replicas.
