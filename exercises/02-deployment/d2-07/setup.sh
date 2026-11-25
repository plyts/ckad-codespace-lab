# Préparation de d2-07 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: web-blue, labels: {app: web, version: blue}}
spec:
  replicas: 2
  selector: {matchLabels: {app: web, version: blue}}
  template:
    metadata: {labels: {app: web, version: blue}}
    spec:
      containers:
      - {name: web, image: "hashicorp/http-echo:1.0.0", args: ["-text=blue"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: web}
spec:
  selector: {app: web, version: blue}
  ports: [{port: 80, targetPort: 5678}]
EOF
