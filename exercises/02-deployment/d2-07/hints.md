## Indice 1

Copie le Deployment blue : `kubectl -n d2-07 get deploy web-blue -o yaml > green.yaml`, puis remplace blue par green (nom, labels, sélecteur, argument).

## Indice 2

Nettoie le YAML copié (status, uid, resourceVersion, creationTimestamp) ou repars de `kubectl create deployment --dry-run=client -o yaml`.

## Indice 3

Bascule : `kubectl -n d2-07 patch svc web -p '{"spec":{"selector":{"app":"web","version":"green"}}}'`.

