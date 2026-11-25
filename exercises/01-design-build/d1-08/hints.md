## Indice 1

Pas de `kubectl create daemonset` : génère un Deployment avec `--dry-run=client -o yaml`, change `kind` et retire `replicas` et `strategy`.

## Indice 2

Taint du control-plane : `node-role.kubernetes.io/control-plane:NoSchedule`.

## Indice 3

`tolerations: - key: node-role.kubernetes.io/control-plane  operator: Exists  effect: NoSchedule`

