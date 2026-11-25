## Indice 1

Commandes impératives utiles : `create configmap`, `create secret generic`, `set env --from=secret/…`, `set resources`, `scale`.

## Indice 2

`kubectl -n boutique-j2 set env deploy/api --from=secret/redis-auth --prefix=REDIS_` crée REDIS_PASSWORD.

## Indice 3

Le volume se monte avec `kubectl edit deploy front` (ou `kubectl set volume` n'existe pas : passe par le YAML).

