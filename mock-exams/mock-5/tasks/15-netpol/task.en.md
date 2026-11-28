---
id: m5-15
title: NetworkPolicy
---
In namespace `m5-15`, create NetworkPolicy `secrets-api-access`: Pods `app=secrets-api` accept incoming
traffic **only** from Pods labelled `access=granted`, on port `80`. Everything else is denied for
those Pods.
