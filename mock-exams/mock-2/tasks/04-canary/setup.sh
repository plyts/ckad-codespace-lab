# Préparation de m2-04 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: search-stable}
spec:
  replicas: 4
  selector: {matchLabels: {app: search, track: stable}}
  template:
    metadata: {labels: {app: search, track: stable}}
    spec:
      containers:
      - {name: search-stable, image: "hashicorp/http-echo:1.0.0", args: ["-text=search v1"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: search}
spec:
  selector: {app: search}
  ports: [{port: 80, targetPort: 5678}]
EOF
k rollout status deploy/search-stable --timeout=180s
