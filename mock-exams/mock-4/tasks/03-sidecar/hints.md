## Indice 1

Le sidecar va sous `initContainers` avec `restartPolicy: Always`.

## Indice 2

Volume : `volumes: [{name: shared, emptyDir: {}}]`, monté sur `/trail` dans les deux conteneurs.

## Indice 3

Vérifie : `kubectl -n m4-03 logs trail -c reader`.

