#!/usr/bin/env bash
# Reference solution: d4-03 — Dedicated ServiceAccount
kubectl config use-context ckad-a
kubectl -n d4-03 create serviceaccount deployer
cat > tool.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: tool
  namespace: d4-03
spec:
  serviceAccountName: deployer
  automountServiceAccountToken: false
  containers:
  - name: tool
    image: busybox:1.37
    command: ["sh", "-c", "sleep 3600"]
EOF
kubectl apply -f tool.yaml
kubectl -n d4-03 wait --for=condition=Ready pod/tool --timeout=60s
