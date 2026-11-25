# Préparation de d5-04 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: shop}
spec:
  replicas: 2
  selector: {matchLabels: {app: shop}}
  template:
    metadata: {labels: {app: shop}}
    spec:
      containers:
      - {name: shop, image: "hashicorp/http-echo:1.0.0", args: ["-text=shop ok"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: shop}
spec:
  selector: {app: shopp}
  ports: [{port: 80, targetPort: 8080}]
EOF
