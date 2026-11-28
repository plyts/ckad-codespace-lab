## Hint 1

`kubectl create secret generic … --from-literal=…`

## Hint 2

`volumes: [{name: creds, secret: {secretName: …}}]`

## Hint 3

`volumeMounts: [{name: creds, mountPath: /etc/creds, readOnly: true}]`

