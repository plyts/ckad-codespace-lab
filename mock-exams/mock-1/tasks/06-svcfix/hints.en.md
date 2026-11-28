## Hint 1

`kubectl get endpointslices`

## Hint 2

Compare the Service selector with the Pod labels; compare targetPort with containerPort.

## Hint 3

`kubectl get endpointslices -l kubernetes.io/service-name=… -o jsonpath='{.items[*].endpoints[*].addresses[*]}'`

