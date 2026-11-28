---
id: m3-12
title: Ingress NetworkPolicy
---
In namespace `m3-12`, create NetworkPolicy `ledger-access`: Pods `app=ledger` accept incoming
traffic **only** from Pods labelled `role=accounting`, on port `80`. Everything else is denied for
those Pods.
