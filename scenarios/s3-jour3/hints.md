## Indice 1

`kubectl -n boutique-j3 get pods -l app=api` puis `kubectl -n boutique-j3 logs <pod-en-erreur>`.

## Indice 2

`kubectl -n boutique-j3 rollout history deploy/api` : le motif de chaque révision est affiché.

## Indice 3

`kubectl -n boutique-j3 rollout undo deploy/api`

