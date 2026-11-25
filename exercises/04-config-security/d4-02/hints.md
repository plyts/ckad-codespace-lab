## Indice 1

Un Secret générique se crée comme une ConfigMap : `kubectl create secret generic --help` (`--from-literal`). Attention au `!` en bash : guillemets simples.

## Indice 2

Le Pod : `kubectl run … --dry-run=client -o yaml`, puis ajoute `env` avec `valueFrom.secretKeyRef`.

## Indice 3

Vérifie : `kubectl -n d4-02 exec db-client -- printenv DB_PASSWORD`.

