---
id: d2-07
title: Blue/green switch
---
In namespace `d2-07`, the **blue** version of the app runs (Deployment `web-blue`) and Service `web`
sends it the traffic.

1. Deploy the **green** version: Deployment `web-green`, 2 replicas, image
   `hashicorp/http-echo:1.0.0` with the argument `-text=green`, port 5678, labels `app=web` and
   `version=green`.
2. Once green is ready, **switch all the traffic** of Service `web` to green.
3. Keep `web-blue` in place (rollback possible).
