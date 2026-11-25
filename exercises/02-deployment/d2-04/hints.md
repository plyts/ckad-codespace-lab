## Indice 1

Regarde les Pods : `kubectl -n d2-04 get pods`, puis `describe` sur un Pod en erreur.

## Indice 2

`kubectl -n d2-04 rollout history deploy/front` montre les révisions.

## Indice 3

`kubectl -n d2-04 rollout undo deploy/front`

