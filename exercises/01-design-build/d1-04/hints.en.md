## Hint 1

You need YAML: generate a Pod with `kubectl run logger --image=busybox:1.37 --dry-run=client -o yaml`, then complete it.

## Hint 2

A native sidecar is declared under `initContainers:` with `restartPolicy: Always`. The volume: `volumes: - name: logs  emptyDir: {}`.

## Hint 3

Both containers have `volumeMounts: - name: logs  mountPath: /var/log/app`.

