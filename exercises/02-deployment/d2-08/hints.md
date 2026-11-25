## Indice 1

Le Service sélectionne seulement `app=api` : tout Pod avec ce label reçoit du trafic.

## Indice 2

Crée `api-v2` (1 réplica) puis `kubectl -n d2-08 scale deploy api-v1 --replicas=4`.

## Indice 3

Vérifie : `kubectl -n d2-08 get endpointslices -l kubernetes.io/service-name=api`.

