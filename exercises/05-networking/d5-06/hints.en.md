## Hint 1

Copy the examples from the "Network Policies" page: there is a "default deny all ingress traffic".

## Hint 2

`allow-frontend`: `podSelector: {matchLabels: {app: api}}`, `ingress: - from: - podSelector: {matchLabels: {role: frontend}}  ports: - port: 80`.

## Hint 3

NetworkPolicies add up: a single rule allowing the traffic is enough.

