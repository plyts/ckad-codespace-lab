# Préparation de d3-03 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: api}
spec:
  replicas: 2
  selector: {matchLabels: {app: api}}
  template:
    metadata: {labels: {app: api}}
    spec:
      containers:
      - {name: api, image: "hashicorp/http-echo:1.0.0", args: ["-text=api"], ports: [{containerPort: 5678}]}
EOF
