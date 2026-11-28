## Hint 1

`kubectl -n d5-04 get endpointslices`: empty = the selector finds no Pod.

## Hint 2

Compare `kubectl -n d5-04 get svc shop -o yaml` and `kubectl -n d5-04 get pods --show-labels`.

## Hint 3

Two mistakes: the selector AND the targetPort.

