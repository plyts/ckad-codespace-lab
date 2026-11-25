## Indice 1

`kubectl -n d3-06 describe pod big` : section Events en bas.

## Indice 2

Pour recréer : `kubectl -n d3-06 get pod big -o yaml > big.yaml`, corrige, puis `kubectl replace --force -f big.yaml`.

## Indice 3

`50` CPU contre `50m` : le suffixe m signifie millicœurs.

