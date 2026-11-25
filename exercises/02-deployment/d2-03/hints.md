## Indice 1

`kubectl set image deploy/front <conteneur>=<image>` : le conteneur s'appelle `nginx`.

## Indice 2

`kubectl annotate deploy front kubernetes.io/change-cause='passage en 1.28'`

## Indice 3

`kubectl -n d2-03 rollout history deploy/front` doit afficher le motif en révision 2.

