---
id: d3-02
title: HTTP liveness probe
---
In namespace `d3-02`, create a Pod `web` (image `nginx:1.27-alpine`) with an HTTP **liveness probe**
`GET /` on port `80`, starting after **5 seconds** and running every **10 seconds**.
