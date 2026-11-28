## Hint 1

Copy the example from the "Network Policies" docs.

## Hint 2

`podSelector: {matchLabels: {app: …}}` + `policyTypes: [Ingress]`.

## Hint 3

`ingress: - from: - podSelector: …  ports: - port: …`

