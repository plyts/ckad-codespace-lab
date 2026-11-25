## Indice 1

Le ServiceAccount se crée en une commande impérative (`kubectl create serviceaccount --help`) ; le Pod demande un YAML.

## Indice 2

Dans le Pod : `serviceAccountName: deployer` et `automountServiceAccountToken: false` sous `spec`.

## Indice 3

Le champ du Pod est immuable : supprime et recrée le Pod si tu t'es trompé.

