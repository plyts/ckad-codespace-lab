## Indice 1

`kubectl get endpointslices`

## Indice 2

Compare sélecteur du Service et labels des Pods ; compare targetPort et containerPort.

## Indice 3

`kubectl get endpointslices -l kubernetes.io/service-name=… -o jsonpath='{.items[*].endpoints[*].addresses[*]}'`

