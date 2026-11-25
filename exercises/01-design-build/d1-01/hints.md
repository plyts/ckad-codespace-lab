## Indice 1

`kubectl run` crée un Pod. Regarde `kubectl run --help` : options `--image`, `--labels`, `--port`.

## Indice 2

N'oublie pas le namespace : `-n d1-01`.

## Indice 3

`kubectl -n d1-01 run web --image=nginx:1.27-alpine --labels=app=web --port=80`

