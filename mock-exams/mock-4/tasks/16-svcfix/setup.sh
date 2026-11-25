# Préparation de m4-16 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: orders}
spec:
  replicas: 2
  selector: {matchLabels: {app: orders, tier: api}}
  template:
    metadata: {labels: {app: orders, tier: api}}
    spec:
      containers:
      - {name: orders, image: "hashicorp/http-echo:1.0.0", args: ["-text=orders ok"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: orders}
spec:
  selector: {app: orders, tier: backend}
  ports: [{name: http, port: 80, targetPort: 8080}]
EOF
k rollout status deploy/orders --timeout=180s
