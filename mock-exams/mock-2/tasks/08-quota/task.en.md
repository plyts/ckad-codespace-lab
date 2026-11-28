---
id: m2-08
title: ResourceQuota
---
In namespace `m2-08`, create ResourceQuota `team-quota`: at most `4` Pods, `requests.cpu=800m`,
`requests.memory=512Mi`. Then create Pod `probe` (`nginx:1.27-alpine`) with requests `100m` / `64Mi`:
it must be accepted.
