# Préparation de m3-08 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: web}
spec:
  replicas: 1
  selector: {matchLabels: {app: web}}
  template:
    metadata: {labels: {app: web}}
    spec:
      containers:
      - {name: web, image: "hashicorp/http-echo:1.0.0", args: ["-text=web ok"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: web}
spec:
  selector: {app: web}
  ports: [{port: 80, targetPort: 5678}]
EOF

mkdir -p "$OUT"
cat > "$OUT/ingress.yaml" <<'EOF'
apiVersion: networking.k8s.io/v1beta1
kind: Ingress
metadata:
  name: legacy-web
  namespace: m3-08
spec:
  ingressClassName: traefik
  rules:
  - host: legacy.m3.lab.local
    http:
      paths:
      - path: /
        backend:
          serviceName: web
          servicePort: 80
EOF
  k rollout status deploy/web --timeout=180s
