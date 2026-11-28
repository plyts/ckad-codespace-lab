---
id: m4-13
title: Quota
---
In namespace `m4-13`, create ResourceQuota `team-quota`: at most `6` Pods, `requests.cpu=1`,
`requests.memory=1Gi`. Then create Pod `probe` (`nginx:1.27-alpine`) with requests `100m` / `64Mi`:
it must be accepted.
