---
id: m4-06
title: 20% canary
---
In namespace `m4-06`, Service `pricing` serves 5 Pods `pricing-stable`. Deploy a canary
`pricing-canary` (`hashicorp/http-echo:1.0.0`, `-text=pricing v2`, port 5678, labels `app=pricing`,
`track=canary`) so that **1 Pod(s) out of 5** behind the Service run v2. The total
number of Pods stays 5.
