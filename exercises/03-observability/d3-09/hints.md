## Indice 1

`kubectl -n d3-09 get events --sort-by=.lastTimestamp | grep -i unhealthy`

## Indice 2

Compare le port de la sonde et le `containerPort` du conteneur.

## Indice 3

`kubectl -n d3-09 edit deploy orders` : corrige le port et ajoute `startupProbe` au même niveau que `livenessProbe`.

