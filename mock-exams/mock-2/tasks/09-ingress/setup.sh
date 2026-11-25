# Préparation de m2-09 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: home}
spec:
  replicas: 1
  selector: {matchLabels: {app: home}}
  template:
    metadata: {labels: {app: home}}
    spec:
      containers:
      - {name: home, image: "hashicorp/http-echo:1.0.0", args: ["-text=home"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: home}
spec:
  selector: {app: home}
  ports: [{port: 80, targetPort: 5678}]
---
apiVersion: apps/v1
kind: Deployment
metadata: {name: docs}
spec:
  replicas: 1
  selector: {matchLabels: {app: docs}}
  template:
    metadata: {labels: {app: docs}}
    spec:
      containers:
      - {name: docs, image: "hashicorp/http-echo:1.0.0", args: ["-text=docs"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: docs}
spec:
  selector: {app: docs}
  ports: [{port: 9090, targetPort: 5678}]
EOF
k rollout status deploy/home --timeout=180s
k rollout status deploy/docs --timeout=180s
