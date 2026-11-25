# Préparation de d5-09 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: catalog}
spec:
  replicas: 2
  selector: {matchLabels: {app: catalog}}
  template:
    metadata: {labels: {app: catalog}}
    spec:
      containers:
      - {name: catalog, image: "hashicorp/http-echo:1.0.0", args: ["-text=catalog ok"], ports: [{containerPort: 5678}]}
EOF
