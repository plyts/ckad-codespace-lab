---
id: m2-04
title: 25% canary
---
In namespace `m2-04`, Service `search` serves 4 Pods `search-stable`. Deploy a canary
`search-canary` (`hashicorp/http-echo:1.0.0`, `-text=search v2`, port 5678, labels `app=search`,
`track=canary`) so that **1 Pod(s) out of 4** behind the Service run v2. The total
number of Pods stays 4.
