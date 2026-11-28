## Hint 1

`create configmap --from-literal`, `create secret generic --from-literal`.

## Hint 2

`env: - name: LOG_LEVEL  valueFrom: configMapKeyRef: {name, key}`

## Hint 3

Same with `secretKeyRef`.

