## Hint 1

`kubectl create quota --hard=…`

## Hint 2

`kubectl run probe … --dry-run=client -o yaml` then add `resources.requests`.

## Hint 3

There is no `kubectl set resources` for a bare Pod: go through the YAML.

