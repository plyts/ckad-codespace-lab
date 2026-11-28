#!/usr/bin/env bash
# Reference solution: d3-02 — HTTP liveness probe
kubectl config use-context ckad-a
cat > web.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: web
  namespace: d3-02
spec:
  containers:
  - name: web
    image: nginx:1.27-alpine
    livenessProbe:
      httpGet:
        path: /
        port: 80
      initialDelaySeconds: 5
      periodSeconds: 10
EOF
kubectl apply -f web.yaml
kubectl -n d3-02 wait --for=condition=Ready pod/web --timeout=90s
