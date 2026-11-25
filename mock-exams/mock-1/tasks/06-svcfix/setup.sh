# Préparation de m1-06 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: inventory}
spec:
  replicas: 2
  selector: {matchLabels: {app: inventory, tier: api}}
  template:
    metadata: {labels: {app: inventory, tier: api}}
    spec:
      containers:
      - {name: inventory, image: "hashicorp/http-echo:1.0.0", args: ["-text=inventory ok"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: inventory}
spec:
  selector: {app: inventory, tier: backend}
  ports: [{name: http, port: 80, targetPort: 8080}]
EOF
k rollout status deploy/inventory --timeout=180s
