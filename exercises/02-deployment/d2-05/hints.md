## Indice 1

`kubectl -n d2-05 edit deploy api` ou `kubectl patch`.

## Indice 2

Tous ces champs sont sous `spec` du Deployment : `strategy.rollingUpdate`, `minReadySeconds`, `revisionHistoryLimit`.

## Indice 3

`kubectl explain deploy.spec --recursive | less` pour retrouver les noms exacts.

