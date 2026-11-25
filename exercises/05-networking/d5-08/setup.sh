# Préparation de d5-08 (CTX, NS, OUT fournis par le lanceur)
k(){ kubectl --context "$CTX" -n "$NS" "$@"; }
k apply -f - <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata: {name: blog}
spec:
  replicas: 1
  selector: {matchLabels: {app: blog}}
  template:
    metadata: {labels: {app: blog}}
    spec:
      containers:
      - {name: blog, image: "hashicorp/http-echo:1.0.0", args: ["-text=blog ok"], ports: [{containerPort: 5678}]}
---
apiVersion: v1
kind: Service
metadata: {name: blog}
spec:
  selector: {app: blog}
  ports: [{port: 80, targetPort: 5678}]
---
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata: {name: blog}
spec:
  ingressClassName: nginx
  rules:
  - host: blog.lab.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service: {name: blog, port: {number: 8080}}
EOF
