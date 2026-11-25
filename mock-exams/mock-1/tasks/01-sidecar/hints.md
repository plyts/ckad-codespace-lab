## Indice 1

Le sidecar va sous `initContainers` avec `restartPolicy: Always`.

## Indice 2

Volume : `volumes: [{name: shared, emptyDir: {}}]`, monté sur `/var/audit` dans les deux conteneurs.

## Indice 3

Vérifie : `kubectl -n m1-01 logs audit -c reader`.

