## Indice 1

`kubectl -n pannes get pods` : chaque statut (CreateContainerConfigError, Pending) oriente le diagnostic.

## Indice 2

`kubectl -n pannes describe pod -l app=orders` et `kubectl -n pannes describe pvc uploads` : lis les Events.

## Indice 3

Pour le PVC : `kubectl -n pannes get pvc uploads -o yaml > pvc.yaml`, change la classe en `standard`, puis supprime et recrée PVC et Pod.

