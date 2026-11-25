## Indice 1

Trois objets, trois commandes : `expose`, `create ingress`, puis un YAML de NetworkPolicy.

## Indice 2

La NetworkPolicy filtre au niveau du Pod : le port est celui du conteneur (5678), pas du Service.

## Indice 3

Le namespace `traefik` porte le label `kubernetes.io/metadata.name=traefik`.

