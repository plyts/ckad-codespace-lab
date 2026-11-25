## Indice 1

Copie la NetworkPolicy d'exemple de la doc et adapte-la quatre fois (une par règle).

## Indice 2

Une NetworkPolicy se pose sur les Pods de **destination** (`podSelector`) et liste les sources autorisées (`from`).

## Indice 3

`kubectl -n boutique-j4 create ingress boutique --class=traefik --rule='boutique.lab.local/*=front:80'`

