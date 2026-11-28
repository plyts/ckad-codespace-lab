## Hint 1

Three objects, three commands: `expose`, `create ingress`, then a NetworkPolicy YAML.

## Hint 2

The NetworkPolicy filters at Pod level: the port is the container's (5678), not the Service's.

## Hint 3

Namespace `traefik` carries the label `kubernetes.io/metadata.name=traefik`.

