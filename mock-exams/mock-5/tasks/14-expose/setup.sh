# Préparation de m5-14 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: ranking}
spec:
  replicas: 2
  selector: {matchLabels: {app: ranking}}
  template:
    metadata: {labels: {app: ranking}}
    spec:
      containers:
      - {name: ranking, image: "hashicorp/http-echo:1.0.0", args: ["-text=ranking ok"], ports: [{containerPort: 5678}]}
EOF
k rollout status deploy/ranking --timeout=180s
