## Indice 1

`kubectl -n d4-05 create quota ns-quota --hard=pods=5,requests.cpu=1,requests.memory=1Gi,limits.cpu=2,limits.memory=2Gi`

## Indice 2

Pas de commande impérative pour la LimitRange : copie l'exemple de la doc « Configure Default Memory Requests and Limits ».

## Indice 3

Si le Pod est refusé (`must specify limits`), la LimitRange manquait au moment de sa création.

