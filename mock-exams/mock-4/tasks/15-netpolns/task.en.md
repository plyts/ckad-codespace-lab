---
id: m4-15
title: NetworkPolicy by namespace
---
In namespace `m4-15`, create NetworkPolicy `from-m4-15-ops`: Pods `app=vault` accept incoming
traffic only from Pods **of namespace `m4-15-ops`** (any Pod).
