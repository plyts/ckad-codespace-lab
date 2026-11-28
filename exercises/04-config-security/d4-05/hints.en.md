## Hint 1

ResourceQuota has an imperative command (`kubectl create quota --help`, option `--hard`); LimitRange does not: copy the docs example "Configure Default Memory Requests and Limits".

## Hint 2

If the Pod is rejected (`must specify limits`), the LimitRange was missing when it was created: order matters.

## Hint 3

`kubectl -n d4-05 create quota ns-quota --hard=pods=5,requests.cpu=1,requests.memory=1Gi,limits.cpu=2,limits.memory=2Gi`

