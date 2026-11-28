## Hint 1

`kubectl -n d3-06 describe pod big`: Events section at the bottom.

## Hint 2

To recreate: `kubectl -n d3-06 get pod big -o yaml > big.yaml`, fix it, then `kubectl replace --force -f big.yaml`.

## Hint 3

`50` CPU versus `50m`: the m suffix means millicores.

