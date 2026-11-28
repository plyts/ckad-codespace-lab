---
id: m3-05
title: Blue/green switch
---
In namespace `m3-05`, the blue and green versions of `checkout` run; Service `checkout` sends everything to
blue. **Switch** the Service to green, then scale `checkout-blue` to 0 replicas (without deleting it).
