# Préparation de m3-13 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: gateway}
spec:
  replicas: 2
  selector: {matchLabels: {app: gateway}}
  template:
    metadata: {labels: {app: gateway}}
    spec:
      containers:
      - {name: gateway, image: "hashicorp/http-echo:1.0.0", args: ["-text=gateway ok"], ports: [{containerPort: 5678}]}
EOF
k rollout status deploy/gateway --timeout=180s
