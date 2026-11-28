---
id: d4-05
title: ResourceQuota and LimitRange
---
In namespace `d4-05`:

1. Create ResourceQuota `ns-quota`: at most `5` Pods, `requests.cpu=1`, `requests.memory=1Gi`,
   `limits.cpu=2`, `limits.memory=2Gi`.
2. Create LimitRange `defaults` giving containers without resources: requests `50m` / `32Mi` and
   limits `100m` / `64Mi`.
3. Check it: create Pod `plain` (`nginx:1.27-alpine`) **without** a `resources` section.
