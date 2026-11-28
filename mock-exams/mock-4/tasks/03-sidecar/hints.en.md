## Hint 1

The sidecar goes under `initContainers` with `restartPolicy: Always`.

## Hint 2

Volume: `volumes: [{name: shared, emptyDir: {}}]`, mounted on `/trail` in both containers.

## Hint 3

Check: `kubectl -n m4-03 logs trail -c reader`.

