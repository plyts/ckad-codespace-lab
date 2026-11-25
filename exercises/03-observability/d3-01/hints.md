## Indice 1

`kubectl -n d3-01 logs talker` affiche la sortie du conteneur.

## Indice 2

`grep SECRET_CODE` puis `cut -d= -f2`.

## Indice 3

`kubectl -n d3-01 logs talker | grep SECRET_CODE | cut -d= -f2 > ~/ckad/d3-01/code.txt`

