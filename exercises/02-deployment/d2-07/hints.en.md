## Hint 1

Copy the blue Deployment: `kubectl -n d2-07 get deploy web-blue -o yaml > green.yaml`, then replace blue with green (name, labels, selector, argument).

## Hint 2

Clean the copied YAML (status, uid, resourceVersion, creationTimestamp) or start from `kubectl create deployment --dry-run=client -o yaml`.

## Hint 3

Switch: `kubectl -n d2-07 patch svc web -p '{"spec":{"selector":{"app":"web","version":"green"}}}'`.

