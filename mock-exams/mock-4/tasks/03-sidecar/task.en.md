---
id: m4-03
title: Native sidecar
---
In namespace `m4-03`, create Pod `trail` with a shared `emptyDir` volume mounted on `/trail`:

- container `writer` (`busybox:1.37`):
  `sh -c 'while true; do echo "trace $(date)" >> /trail/out.log; sleep 2; done'`
- **native sidecar** `reader` (`busybox:1.37`): `sh -c 'tail -F /trail/out.log'`
