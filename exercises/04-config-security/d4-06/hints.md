## Indice 1

Deux `securityContext` : un sous `spec` (Pod), un sous le conteneur.

## Indice 2

Pod : `runAsUser`, `runAsGroup`, `fsGroup`. Conteneur : `allowPrivilegeEscalation`, `readOnlyRootFilesystem`, `capabilities`.

## Indice 3

Vérifie : `kubectl -n d4-06 exec secure -- id`.

