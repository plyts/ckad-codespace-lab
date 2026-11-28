## Hint 1

`kubectl -n d3-09 get events --sort-by=.lastTimestamp | grep -i unhealthy`

## Hint 2

Compare the probe port and the container's `containerPort`.

## Hint 3

`kubectl -n d3-09 edit deploy orders`: fix the port and add `startupProbe` at the same level as `livenessProbe`.

