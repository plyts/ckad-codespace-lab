## Hint 1

`kubectl describe pod`: Events.

## Hint 2

Look at `spec.nodeSelector`.

## Hint 3

`kubectl get pod -o yaml > f.yaml`, remove the nodeSelector, `kubectl replace --force -f f.yaml`.

