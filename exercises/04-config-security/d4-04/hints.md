## Indice 1

`kubectl run bounded --image=nginx:1.27-alpine --dry-run=client -o yaml` puis ajoute `resources`.

## Indice 2

`resources: {requests: {cpu: 100m, memory: 64Mi}, limits: {cpu: 200m, memory: 128Mi}}`

## Indice 3

`kubectl get pod bounded -o jsonpath='{.status.qosClass}'`

