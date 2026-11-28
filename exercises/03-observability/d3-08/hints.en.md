## Hint 1

`kubectl top pods -n d3-08`

## Hint 2

Option `--sort-by=cpu`.

## Hint 3

`kubectl -n d3-08 top pods --sort-by=cpu --no-headers | head -1 | awk '{print $1}' > ~/ckad/d3-08/top.txt`

