## Indice 1

Le format est `<service>.<namespace>.svc.cluster.local`.

## Indice 2

`kubectl -n d5-03 get svc db -o jsonpath='{.spec.clusterIP}' > ~/ckad/d5-03/ip.txt`

## Indice 3

`kubectl -n d5-03 run t --rm -it --image=busybox:1.37 --restart=Never -- nslookup db`

