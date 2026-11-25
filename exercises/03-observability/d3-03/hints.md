## Indice 1

`kubectl -n d3-03 edit deploy api` : la sonde va dans `spec.template.spec.containers[0]`.

## Indice 2

`readinessProbe: {tcpSocket: {port: 5678}, initialDelaySeconds: 2, periodSeconds: 5}`

## Indice 3

Modifier le template déclenche un rolling update : `kubectl -n d3-03 rollout status deploy/api`.

