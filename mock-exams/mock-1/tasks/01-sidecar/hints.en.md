## Hint 1

The sidecar goes under `initContainers` with `restartPolicy: Always`.

## Hint 2

Volume: `volumes: [{name: shared, emptyDir: {}}]`, mounted on `/var/audit` in both containers.

## Hint 3

Check: `kubectl -n m1-01 logs audit -c reader`.

