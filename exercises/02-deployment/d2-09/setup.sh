# Préparation de d2-09 (CTX, NS, OUT fournis par le lanceur)
mkdir -p "$OUT/base"
cat > "$OUT/base/deployment.yaml" <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web
  labels: {app: web}
spec:
  replicas: 1
  selector: {matchLabels: {app: web}}
  template:
    metadata: {labels: {app: web}}
    spec:
      containers:
      - {name: web, image: "nginx:1.27-alpine", ports: [{containerPort: 80}]}
EOF
cat > "$OUT/base/service.yaml" <<'EOF'
apiVersion: v1
kind: Service
metadata: {name: web}
spec:
  selector: {app: web}
  ports: [{port: 80, targetPort: 80}]
EOF
cat > "$OUT/base/kustomization.yaml" <<'EOF'
resources:
- deployment.yaml
- service.yaml
EOF
