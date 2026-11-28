---
id: m1-01
title: Logging sidecar
---
In namespace `m1-01`, create Pod `audit` with a shared `emptyDir` volume mounted on `/var/audit`:

- container `writer` (`busybox:1.37`):
  `sh -c 'while true; do echo "event $(date)" >> /var/audit/out.log; sleep 2; done'`
- **native sidecar** `reader` (`busybox:1.37`): `sh -c 'tail -F /var/audit/out.log'`
