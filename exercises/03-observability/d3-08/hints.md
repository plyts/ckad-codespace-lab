## Indice 1

`kubectl top pods -n d3-08`

## Indice 2

Option `--sort-by=cpu`.

## Indice 3

`kubectl -n d3-08 top pods --sort-by=cpu --no-headers | head -1 | awk '{print $1}' > ~/ckad/d3-08/top.txt`

