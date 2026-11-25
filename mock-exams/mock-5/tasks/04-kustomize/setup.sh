# Préparation de m5-04 (CTX, NS, OUT fournis par le lanceur)
mkdir -p "$OUT/base"
cat > "$OUT/base/app.yaml" <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: shop}
spec:
  replicas: 1
  selector: {matchLabels: {app: shop}}
  template:
    metadata: {labels: {app: shop}}
    spec:
      containers: [{name: shop, image: "nginx:1.27-alpine"}]
EOF
printf 'resources:\n- app.yaml\n' > "$OUT/base/kustomization.yaml"
