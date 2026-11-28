## Hint 1

Generate a Deployment, change to `kind: DaemonSet`, remove `replicas` and `strategy`.

## Hint 2

Toleration: `key: node-role.kubernetes.io/control-plane, operator: Exists, effect: NoSchedule`.

## Hint 3

`kubectl rollout status ds/<name>`

