## Hint 1

`kubectl -n d2-05 edit deploy api` or `kubectl patch`.

## Hint 2

All these fields are under the Deployment's `spec`: `strategy.rollingUpdate`, `minReadySeconds`, `revisionHistoryLimit`.

## Hint 3

`kubectl explain deploy.spec --recursive | less` to find the exact names.

