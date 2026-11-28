## Hint 1

`kubectl create job … --dry-run=client -o yaml -- sh -c '…'` then edit.

## Hint 2

`completions`, `parallelism` and `backoffLimit` are under `spec` (not under `template`).

## Hint 3

`kubectl wait --for=condition=Complete job/<name>`

