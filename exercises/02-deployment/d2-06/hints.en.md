## Hint 1

`helm install --help`: `-n`, `--set`, and the chart path as second argument.

## Hint 2

`helm -n d2-06 install shop ~/ckad/d2-06/webapp --set replicaCount=2 --set image.tag=1.28-alpine`

## Hint 3

`helm show values ~/ckad/d2-06/webapp > ~/ckad/d2-06/values.txt`

