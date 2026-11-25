## Indice 1

`kubectl apply -f ~/ckad/d3-07/old.yaml` : lis bien le message d'erreur.

## Indice 2

`kubectl api-resources | grep -E 'cronjob|poddisruption'` donne le groupe/version actuel.

## Indice 3

`kubectl explain cronjob` affiche la VERSION en tête.

