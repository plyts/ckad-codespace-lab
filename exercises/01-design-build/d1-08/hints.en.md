## Hint 1

No `kubectl create daemonset`: generate a Deployment with `--dry-run=client -o yaml`, change `kind` and remove `replicas` and `strategy`.

## Hint 2

Control-plane taint: `node-role.kubernetes.io/control-plane:NoSchedule`.

## Hint 3

`tolerations: - key: node-role.kubernetes.io/control-plane  operator: Exists  effect: NoSchedule`

