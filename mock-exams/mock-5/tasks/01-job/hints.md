## Indice 1

`kubectl create job … --dry-run=client -o yaml -- sh -c '…'` puis édite.

## Indice 2

`completions`, `parallelism` et `backoffLimit` sont sous `spec` (pas sous `template`).

## Indice 3

`kubectl wait --for=condition=Complete job/<nom>`

