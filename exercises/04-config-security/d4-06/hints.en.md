## Hint 1

Two `securityContext` blocks: one under `spec` (Pod), one under the container.

## Hint 2

Pod: `runAsUser`, `runAsGroup`, `fsGroup`. Container: `allowPrivilegeEscalation`, `readOnlyRootFilesystem`, `capabilities`.

## Hint 3

Check: `kubectl -n d4-06 exec secure -- id`.

