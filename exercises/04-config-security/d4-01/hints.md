## Indice 1

`kubectl create configmap --help` : `--from-literal=CLÉ=valeur` (répétable).

## Indice 2

Pour le Pod, génère le YAML avec `kubectl run … --dry-run=client -o yaml` et ajoute `envFrom`.

## Indice 3

`envFrom: - configMapRef: {name: app-config}`

