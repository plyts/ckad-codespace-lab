## Hint 1

`kubectl create configmap --help`: `--from-literal=KEY=value` (repeatable).

## Hint 2

For the Pod, generate the YAML with `kubectl run … --dry-run=client -o yaml` and add `envFrom`.

## Hint 3

`envFrom: - configMapRef: {name: app-config}`

