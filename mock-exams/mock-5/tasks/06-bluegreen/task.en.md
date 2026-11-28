---
id: m5-06
title: Blue/green
---
In namespace `m5-06`, the blue and green versions of `profile` run; Service `profile` sends everything to
blue. **Switch** the Service to green, then scale `profile-blue` to 0 replicas (without deleting it).
