## Indice 1

`kubectl create deployment … --replicas=N` puis `kubectl expose deploy … --port=… --target-port=…` : 6 commandes au total.

## Indice 2

Pour l'argument de http-echo : `kubectl create deployment api --image=hashicorp/http-echo:1.0.0 --replicas=2 -- /http-echo -text='api v1'`.

## Indice 3

Test : `kubectl -n boutique-j1 run t --rm -i --image=busybox:1.37 --restart=Never -- wget -qO- http://api`.

