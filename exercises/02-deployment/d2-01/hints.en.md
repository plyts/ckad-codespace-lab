## Hint 1

`kubectl create deployment --help`: options `--image` and `--replicas`.

## Hint 2

`kubectl -n d2-01 create deployment front --image=nginx:1.27-alpine --replicas=3`

## Hint 3

Follow the rollout: `kubectl -n d2-01 rollout status deploy/front`.

