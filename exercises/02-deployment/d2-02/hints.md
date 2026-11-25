## Indice 1

Une seule commande suffit : `kubectl scale`.

## Indice 2

`kubectl -n d2-02 scale deploy front --replicas=5`

## Indice 3

Alternative : `kubectl -n d2-02 edit deploy front` et changer `spec.replicas`.

