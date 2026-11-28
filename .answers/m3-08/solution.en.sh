#!/usr/bin/env bash
# Reference solution: m3-08 — Ingress on a removed API
kubectl config use-context ckad-a

cat > ~/ckad/m3-08/ingress.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
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
        pathType: Prefix
        backend:
          service:
            name: web
            port: {number: 80}
EOF
kubectl apply -f ~/ckad/m3-08/ingress.yaml
