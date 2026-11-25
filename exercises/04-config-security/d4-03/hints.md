## Indice 1

`kubectl -n d4-03 create serviceaccount deployer`

## Indice 2

Dans le Pod : `serviceAccountName: deployer` et `automountServiceAccountToken: false` sous `spec`.

## Indice 3

Le champ du Pod est immuable : supprime et recrée le Pod si tu t'es trompé.

