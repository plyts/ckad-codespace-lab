## Hint 1

`kubectl -n d3-03 edit deploy api`: the probe goes into `spec.template.spec.containers[0]`.

## Hint 2

`readinessProbe: {tcpSocket: {port: 5678}, initialDelaySeconds: 2, periodSeconds: 5}`

## Hint 3

Changing the template triggers a rolling update: `kubectl -n d3-03 rollout status deploy/api`.

