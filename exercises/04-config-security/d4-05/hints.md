## Indice 1

La ResourceQuota a une commande impérative (`kubectl create quota --help`, option `--hard`) ; la LimitRange, non : copie l'exemple de la doc « Configure Default Memory Requests and Limits ».

## Indice 2

Si le Pod est refusé (`must specify limits`), la LimitRange manquait au moment de sa création : l'ordre compte.

## Indice 3

`kubectl -n d4-05 create quota ns-quota --hard=pods=5,requests.cpu=1,requests.memory=1Gi,limits.cpu=2,limits.memory=2Gi`

