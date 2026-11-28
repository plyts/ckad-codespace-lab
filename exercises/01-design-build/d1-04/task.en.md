---
id: d1-04
title: Sidecar following a log file
---
In namespace `d1-04`, create a Pod `logger` with two containers sharing an `emptyDir` volume named
`logs`, mounted on `/var/log/app`:

- main container `app`, image `busybox:1.37`, writing a line every 2 seconds:
  `sh -c 'while true; do echo "tick $(date)" >> /var/log/app/app.log; sleep 2; done'`
- sidecar container `shipper`, image `busybox:1.37`, printing that file continuously:
  `sh -c 'tail -F /var/log/app/app.log'`

Use a **native sidecar** (an init container restarted continuously).
`kubectl logs logger -c shipper` must show the `tick` lines.
