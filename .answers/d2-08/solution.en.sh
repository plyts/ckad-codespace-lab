#!/usr/bin/env bash
# Reference solution: d2-08 — 20% canary
kubectl config use-context ckad-a
cat > canary.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: api-v2
  namespace: d2-08
spec:
  replicas: 1
  selector:
    matchLabels: {app: api, track: canary}
  template:
    metadata:
      labels: {app: api, track: canary}
    spec:
      containers:
      - name: api
        image: hashicorp/http-echo:1.0.0
        args: ["-text=api v2"]
        ports:
        - containerPort: 5678
EOF
kubectl apply -f canary.yaml
kubectl -n d2-08 scale deploy api-v1 --replicas=4
kubectl -n d2-08 rollout status deploy/api-v2 --timeout=120s
# Test: for i in $(seq 10); do kubectl -n d2-08 exec deploy/api-v1 -- ... ; done is not possible (image without a shell):
# kubectl -n d2-08 run t --rm -it --image=busybox:1.37 --restart=Never -- sh -c 'for i in $(seq 10); do wget -qO- api; done'
