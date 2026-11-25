# Préparation de d2-08 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }

k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: api-v1}
spec:
  replicas: 5
  selector: {matchLabels: {app: api, track: stable}}
  template:
    metadata: {labels: {app: api, track: stable}}
    spec:
      containers:
      - {name: api, image: "hashicorp/http-echo:1.0.0", args: ["-text=api v1"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: api}
spec:
  selector: {app: api}
  ports: [{port: 80, targetPort: 5678}]
EOF
