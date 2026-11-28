## Hint 1

Three imperative commands: `create configmap --from-literal`, `create secret generic --from-literal`, `create serviceaccount`.

## Hint 2

Generate the Deployment: `kubectl -n d4-09 create deployment portal --image=nginx:1.27-alpine --replicas=2 --dry-run=client -o yaml > portal.yaml`.

## Hint 3

Add `serviceAccountName`, `volumes` (configMap), `volumeMounts`, `env.valueFrom.secretKeyRef` and `resources`.

