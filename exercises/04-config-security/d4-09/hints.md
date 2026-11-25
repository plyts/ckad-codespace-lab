## Indice 1

Trois commandes impératives : `create configmap --from-literal`, `create secret generic --from-literal`, `create serviceaccount`.

## Indice 2

Génère le Deployment : `kubectl -n d4-09 create deployment portal --image=nginx:1.27-alpine --replicas=2 --dry-run=client -o yaml > portal.yaml`.

## Indice 3

Ajoute `serviceAccountName`, `volumes` (configMap), `volumeMounts`, `env.valueFrom.secretKeyRef` et `resources`.

