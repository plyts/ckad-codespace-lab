## Hint 1

No imperative command for a PVC: copy the example from the docs ("PersistentVolumeClaims").

## Hint 2

The Pod declares `volumes: - name: data  persistentVolumeClaim: { claimName: data }` then a `volumeMounts` on `/data`.

## Hint 3

A Pending PVC with `WaitForFirstConsumer` is normal as long as the Pod does not exist.

