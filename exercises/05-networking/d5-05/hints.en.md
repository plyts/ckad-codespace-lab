## Hint 1

`kubectl create ingress --help`: option `--rule=host/path*=service:port` (the star = Prefix).

## Hint 2

`--class=traefik`

## Hint 3

`kubectl -n d5-05 create ingress shop --class=traefik --rule='shop.lab.local/*=front:80' --rule='shop.lab.local/api*=api:8080'`

