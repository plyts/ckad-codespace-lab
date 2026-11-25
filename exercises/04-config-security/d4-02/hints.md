## Indice 1

`kubectl create secret generic db-cred --from-literal=username=admin --from-literal='password=S3cr3t!'` (guillemets simples à cause du `!`).

## Indice 2

Le Pod : `kubectl run … --dry-run=client -o yaml`, puis ajoute `env` avec `valueFrom.secretKeyRef`.

## Indice 3

Vérifie : `kubectl -n d4-02 exec db-client -- printenv DB_PASSWORD`.

