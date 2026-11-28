## Hint 1

`kubectl -n d3-05 get pods` then `describe`: the Events section gives the exact message.

## Hint 2

The container is named `redis` (name derived from the image by `kubectl create deployment`).

## Hint 3

`kubectl -n d3-05 set image deploy/cache redis=redis:7.4-alpine`

