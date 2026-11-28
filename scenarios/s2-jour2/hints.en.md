## Hint 1

Useful imperative commands: `create configmap`, `create secret generic`, `set env --from=secret/…`, `set resources`, `scale`.

## Hint 2

`kubectl -n boutique-j2 set env deploy/api --from=secret/redis-auth --prefix=REDIS_` creates REDIS_PASSWORD.

## Hint 3

The volume is mounted with `kubectl edit deploy front` (there is no `kubectl set volume`: go through the YAML).

