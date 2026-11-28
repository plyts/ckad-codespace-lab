#!/usr/bin/env bash
# Reference solution: d1-08 — DaemonSet on every node
kubectl config use-context ckad-a
cat > ds.yaml <<'EOF'
apiVersion: apps/v1
kind: DaemonSet
metadata:
  name: node-agent
  namespace: d1-08
  labels:
    app: node-agent
spec:
  selector:
    matchLabels:
      app: node-agent
  template:
    metadata:
      labels:
        app: node-agent
    spec:
      tolerations:                       # allows the control-plane node
      - key: node-role.kubernetes.io/control-plane
        operator: Exists
        effect: NoSchedule
      containers:
      - name: agent
        image: busybox:1.37
        command: ["sh", "-c", "sleep 3600"]
EOF
kubectl apply -f ds.yaml
kubectl -n d1-08 rollout status ds/node-agent --timeout=120s
kubectl -n d1-08 get pods -o wide
