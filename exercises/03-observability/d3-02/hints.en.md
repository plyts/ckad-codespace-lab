## Hint 1

Generate the Pod: `kubectl -n d3-02 run web --image=nginx:1.27-alpine --dry-run=client -o yaml > web.yaml`.

## Hint 2

Under the container: `livenessProbe: {httpGet: {path: /, port: 80}, initialDelaySeconds: 5, periodSeconds: 10}`.

## Hint 3

Search "liveness" in kubernetes.io/docs: the page "Configure Liveness, Readiness and Startup Probes" has ready-made examples.

