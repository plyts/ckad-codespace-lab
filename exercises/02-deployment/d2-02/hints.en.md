## Hint 1

A single command is enough: `kubectl scale`.

## Hint 2

`kubectl -n d2-02 scale deploy front --replicas=5`

## Hint 3

Alternative: `kubectl -n d2-02 edit deploy front` and change `spec.replicas`.

