## Indice 1

Génère le Pod : `kubectl -n d3-02 run web --image=nginx:1.27-alpine --dry-run=client -o yaml > web.yaml`.

## Indice 2

Sous le conteneur : `livenessProbe: {httpGet: {path: /, port: 80}, initialDelaySeconds: 5, periodSeconds: 10}`.

## Indice 3

Cherche « liveness » dans kubernetes.io/docs : la page « Configure Liveness, Readiness and Startup Probes » a des exemples prêts.

