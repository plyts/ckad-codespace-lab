## Indice 1

`kubectl expose` sait créer un NodePort (`--type`), mais pas choisir le numéro : génère le YAML avec `--dry-run=client -o yaml`.

## Indice 2

Ajoute `nodePort: 30080` dans `spec.ports[0]`, puis applique.

## Indice 3

`kubectl -n d5-02 expose deploy web --name=web-np --type=NodePort --port=80 --dry-run=client -o yaml > np.yaml`

