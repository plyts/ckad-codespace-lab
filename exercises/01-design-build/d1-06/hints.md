## Indice 1

Pas de commande impérative pour un PVC : copie l'exemple de la doc (« PersistentVolumeClaims »).

## Indice 2

Le Pod déclare `volumes: - name: data  persistentVolumeClaim: { claimName: data }` puis un `volumeMounts` sur `/data`.

## Indice 3

Un PVC Pending avec `WaitForFirstConsumer` est normal tant que le Pod n'existe pas.

