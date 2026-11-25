## Indice 1

Copie les exemples de la page « Network Policies » : il y a un « default deny all ingress traffic ».

## Indice 2

`allow-frontend` : `podSelector: {matchLabels: {app: api}}`, `ingress: - from: - podSelector: {matchLabels: {role: frontend}}  ports: - port: 80`.

## Indice 3

Les NetworkPolicy s'additionnent : une seule règle qui autorise suffit.

