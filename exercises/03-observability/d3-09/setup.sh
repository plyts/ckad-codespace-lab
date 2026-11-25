# Préparation de d3-09 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: orders}
spec:
  replicas: 2
  selector: {matchLabels: {app: orders}}
  template:
    metadata: {labels: {app: orders}}
    spec:
      containers:
      - name: orders
        image: hashicorp/http-echo:1.0.0
        args: ["-text=orders"]
        ports: [{containerPort: 5678}]
        livenessProbe:
          httpGet: {path: /, port: 8080}
          periodSeconds: 3
          failureThreshold: 1
EOF
