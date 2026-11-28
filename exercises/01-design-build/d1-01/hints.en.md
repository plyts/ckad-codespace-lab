## Hint 1

`kubectl run` creates a Pod. See `kubectl run --help`: options `--image`, `--labels`, `--port`.

## Hint 2

Do not forget the namespace: `-n d1-01`.

## Hint 3

`kubectl -n d1-01 run web --image=nginx:1.27-alpine --labels=app=web --port=80`

