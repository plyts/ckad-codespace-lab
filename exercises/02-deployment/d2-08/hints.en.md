## Hint 1

The Service only selects `app=api`: any Pod with that label receives traffic.

## Hint 2

Create `api-v2` (1 replica) then `kubectl -n d2-08 scale deploy api-v1 --replicas=4`.

## Hint 3

Check: `kubectl -n d2-08 get endpointslices -l kubernetes.io/service-name=api`.

