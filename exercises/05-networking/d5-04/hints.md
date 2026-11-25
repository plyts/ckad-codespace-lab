## Indice 1

`kubectl -n d5-04 get endpointslices` : vide = le sélecteur ne trouve aucun Pod.

## Indice 2

Compare `kubectl -n d5-04 get svc shop -o yaml` et `kubectl -n d5-04 get pods --show-labels`.

## Indice 3

Deux erreurs : le sélecteur ET le targetPort.

