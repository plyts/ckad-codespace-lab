## Hint 1

`kubectl set image deploy/front <container>=<image>`: the container is named `nginx`.

## Hint 2

`kubectl annotate deploy front kubernetes.io/change-cause='passage en 1.28'`

## Hint 3

`kubectl -n d2-03 rollout history deploy/front` must show the cause on revision 2.

