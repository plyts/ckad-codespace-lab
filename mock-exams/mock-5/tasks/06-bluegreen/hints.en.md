## Hint 1

`kubectl patch svc … -p '{"spec":{"selector":{…}}}'`

## Hint 2

The patched selector must keep `app` and change `color`.

## Hint 3

`kubectl scale deploy … --replicas=0`

