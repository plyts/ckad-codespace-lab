#!/usr/bin/env bash
# Reference solution: d2-07 — Blue/green switch
kubectl config use-context ckad-a
cat > green.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-green
  namespace: d2-07
  labels: {app: web, version: green}
spec:
  replicas: 2
  selector:
    matchLabels: {app: web, version: green}
  template:
    metadata:
      labels: {app: web, version: green}
    spec:
      containers:
      - name: web
        image: hashicorp/http-echo:1.0.0
        args: ["-text=green"]
        ports:
        - containerPort: 5678
EOF
kubectl apply -f green.yaml
kubectl -n d2-07 rollout status deploy/web-green --timeout=120s
kubectl -n d2-07 patch svc web -p '{"spec":{"selector":{"app":"web","version":"green"}}}'
kubectl -n d2-07 get endpointslices -l kubernetes.io/service-name=web
# Rollback: same patch with "version":"blue".
