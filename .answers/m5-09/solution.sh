#!/usr/bin/env bash
# Solution de référence : m5-09 — API retirée
kubectl config use-context ckad-a

cat > ~/ckad/m5-09/ingress.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: old-site
  namespace: m5-09
spec:
  ingressClassName: traefik
  rules:
  - host: old.m5.lab.local
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: web
            port: {number: 80}
EOF
kubectl apply -f ~/ckad/m5-09/ingress.yaml
