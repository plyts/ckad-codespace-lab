## Hint 1

The overlay references the base by relative path: `resources: [../../base]`.

## Hint 2

Useful fields: `namespace`, `namePrefix`, `labels` (or `commonLabels`), `replicas`.

## Hint 3

Preview before applying: `kubectl kustomize ~/ckad/d2-09/overlays/prod`, then `kubectl apply -k …`.

