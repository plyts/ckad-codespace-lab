# Préparation de m3-05 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: checkout-blue}
spec:
  replicas: 2
  selector: {matchLabels: {app: checkout, color: blue}}
  template:
    metadata: {labels: {app: checkout, color: blue}}
    spec:
      containers:
      - {name: checkout-blue, image: "hashicorp/http-echo:1.0.0", args: ["-text=blue"], ports: [{containerPort: 5678}]}
---
apiVersion: apps/v1
kind: Deployment
metadata: {name: checkout-green}
spec:
  replicas: 2
  selector: {matchLabels: {app: checkout, color: green}}
  template:
    metadata: {labels: {app: checkout, color: green}}
    spec:
      containers:
      - {name: checkout-green, image: "hashicorp/http-echo:1.0.0", args: ["-text=green"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: checkout}
spec:
  selector: {app: checkout, color: blue}
  ports: [{port: 80, targetPort: 5678}]
EOF
k rollout status deploy/checkout-blue --timeout=180s
k rollout status deploy/checkout-green --timeout=180s
