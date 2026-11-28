---
id: d5-04
title: Service without Endpoints
---
In namespace `d5-04`, Service `shop` does not answer, although the Pods of Deployment `shop` run.
Fix **the Service** (not the Deployment): `http://shop.d5-04` must answer `shop ok`.
