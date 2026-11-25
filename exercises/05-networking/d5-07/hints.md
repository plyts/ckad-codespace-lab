## Indice 1

Chaque namespace porte le label automatique `kubernetes.io/metadata.name=<nom>`.

## Indice 2

Dans `to:`, un élément avec `namespaceSelector` ET `podSelector` = les deux conditions à la fois.

## Indice 3

Ajoute une seconde règle egress : `ports: [{protocol: UDP, port: 53}, {protocol: TCP, port: 53}]` sans `to` (n'importe où).

