# Préparation de m4-06 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: pricing-stable}
spec:
  replicas: 5
  selector: {matchLabels: {app: pricing, track: stable}}
  template:
    metadata: {labels: {app: pricing, track: stable}}
    spec:
      containers:
      - {name: pricing-stable, image: "hashicorp/http-echo:1.0.0", args: ["-text=pricing v1"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: pricing}
spec:
  selector: {app: pricing}
  ports: [{port: 80, targetPort: 5678}]
EOF
k rollout status deploy/pricing-stable --timeout=180s
