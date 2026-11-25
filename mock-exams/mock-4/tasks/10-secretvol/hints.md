## Indice 1

`kubectl create secret generic … --from-literal=…`

## Indice 2

`volumes: [{name: creds, secret: {secretName: …}}]`

## Indice 3

`volumeMounts: [{name: creds, mountPath: /etc/creds, readOnly: true}]`

