## Indice 1

`kubectl -n d3-05 get pods` puis `describe` : la section Events donne le message exact.

## Indice 2

Le conteneur s'appelle `redis` (nom tiré de l'image par `kubectl create deployment`).

## Indice 3

`kubectl -n d3-05 set image deploy/cache redis=redis:7.4-alpine`

