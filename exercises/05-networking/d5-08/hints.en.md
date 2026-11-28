## Hint 1

`kubectl get ingressclass`: which classes exist?

## Hint 2

`kubectl -n d5-08 describe ingress blog`: look at the backend and its port, then `kubectl -n d5-08 get svc blog`.

## Hint 3

`kubectl -n d5-08 edit ingress blog`

