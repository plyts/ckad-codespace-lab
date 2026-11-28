## Hint 1

A generic Secret is created like a ConfigMap: `kubectl create secret generic --help` (`--from-literal`). Mind the `!` in bash: single quotes.

## Hint 2

The Pod: `kubectl run … --dry-run=client -o yaml`, then add `env` with `valueFrom.secretKeyRef`.

## Hint 3

Check: `kubectl -n d4-02 exec db-client -- printenv DB_PASSWORD`.

