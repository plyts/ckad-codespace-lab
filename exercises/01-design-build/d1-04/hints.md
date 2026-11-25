## Indice 1

Il faut un YAML : génère un Pod avec `kubectl run logger --image=busybox:1.37 --dry-run=client -o yaml`, puis complète.

## Indice 2

Un sidecar natif se déclare sous `initContainers:` avec `restartPolicy: Always`. Le volume : `volumes: - name: logs  emptyDir: {}`.

## Indice 3

Les deux conteneurs ont `volumeMounts: - name: logs  mountPath: /var/log/app`.

