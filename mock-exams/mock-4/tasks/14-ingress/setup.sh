# Préparation de m4-14 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: shop}
spec:
  replicas: 1
  selector: {matchLabels: {app: shop}}
  template:
    metadata: {labels: {app: shop}}
    spec:
      containers:
      - {name: shop, image: "hashicorp/http-echo:1.0.0", args: ["-text=shop"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: shop}
spec:
  selector: {app: shop}
  ports: [{port: 80, targetPort: 5678}]
---
apiVersion: apps/v1
kind: Deployment
metadata: {name: cart}
spec:
  replicas: 1
  selector: {matchLabels: {app: cart}}
  template:
    metadata: {labels: {app: cart}}
    spec:
      containers:
      - {name: cart, image: "hashicorp/http-echo:1.0.0", args: ["-text=cart"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: cart}
spec:
  selector: {app: cart}
  ports: [{port: 9090, targetPort: 5678}]
EOF
k rollout status deploy/shop --timeout=180s
k rollout status deploy/cart --timeout=180s
