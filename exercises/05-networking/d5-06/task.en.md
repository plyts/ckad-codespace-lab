---
id: d5-06
title: NetworkPolicy: deny then allow
---
In namespace `d5-06`, Service `api` (Pods `app=api`, port 80) is open to everyone.

1. NetworkPolicy `default-deny`: **blocks all incoming traffic** to every Pod of the namespace.
2. NetworkPolicy `allow-frontend`: allows incoming traffic to Pods `app=api` on port `80`, **only**
   from Pods of the namespace labelled `role=frontend`.
