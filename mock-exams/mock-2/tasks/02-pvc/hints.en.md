## Hint 1

Copy the PVC example from the "Persistent Volumes" docs.

## Hint 2

In the Pod: `volumes: [{name: data, persistentVolumeClaim: {claimName: …}}]`.

## Hint 3

A `Pending` PVC without a Pod is normal with `WaitForFirstConsumer`.

