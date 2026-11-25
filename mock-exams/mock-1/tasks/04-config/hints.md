## Indice 1

`create configmap --from-literal`, `create secret generic --from-literal`.

## Indice 2

`env: - name: LOG_LEVEL  valueFrom: configMapKeyRef: {name, key}`

## Indice 3

Idem avec `secretKeyRef`.

