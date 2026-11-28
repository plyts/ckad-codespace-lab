## Hint 1

Every namespace carries the automatic label `kubernetes.io/metadata.name=<name>`.

## Hint 2

In `to:`, one item with `namespaceSelector` AND `podSelector` = both conditions at once.

## Hint 3

Add a second egress rule: `ports: [{protocol: UDP, port: 53}, {protocol: TCP, port: 53}]` without `to` (anywhere).

