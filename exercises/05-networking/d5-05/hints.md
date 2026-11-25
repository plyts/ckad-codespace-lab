## Indice 1

`kubectl create ingress --help` : option `--rule=hôte/chemin*=service:port` (l'étoile = Prefix).

## Indice 2

`--class=traefik`

## Indice 3

`kubectl -n d5-05 create ingress shop --class=traefik --rule='shop.lab.local/*=front:80' --rule='shop.lab.local/api*=api:8080'`

