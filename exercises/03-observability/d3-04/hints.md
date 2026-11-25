## Indice 1

`kubectl -n d3-04 get pods`, puis `kubectl -n d3-04 describe pod <pod>` : regarde « Last State ».

## Indice 2

`kubectl -n d3-04 logs <pod> --previous` montre la sortie du conteneur mort.

## Indice 3

`kubectl -n d3-04 edit deploy worker` et corrige `slep` en `sleep`.

