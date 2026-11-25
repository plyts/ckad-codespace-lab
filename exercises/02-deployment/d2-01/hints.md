## Indice 1

`kubectl create deployment --help` : options `--image` et `--replicas`.

## Indice 2

`kubectl -n d2-01 create deployment front --image=nginx:1.27-alpine --replicas=3`

## Indice 3

Suis la montée : `kubectl -n d2-01 rollout status deploy/front`.

