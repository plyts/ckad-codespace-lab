## Indice 1

Génère un Deployment, change `kind: DaemonSet`, retire `replicas` et `strategy`.

## Indice 2

Toleration : `key: node-role.kubernetes.io/control-plane, operator: Exists, effect: NoSchedule`.

## Indice 3

`kubectl rollout status ds/<nom>`

