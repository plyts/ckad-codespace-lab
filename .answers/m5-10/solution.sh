#!/usr/bin/env bash
# Solution de référence : m5-10 — ConfigMap et Secret
kubectl config use-context ckad-b

kubectl -n m5-10 create configmap agent-cfg --from-literal=LEVEL=warn
kubectl -n m5-10 create secret generic agent-sec --from-literal=TOKEN=s3cr3t-b2
cat > agent.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: agent, namespace: m5-10}
spec:
  containers:
  - name: app
    image: busybox:1.37
    command: ["sh", "-c", "sleep 3600"]
    env:
    - name: LOG_LEVEL
      valueFrom: {configMapKeyRef: {name: agent-cfg, key: LEVEL}}
    - name: API_TOKEN
      valueFrom: {secretKeyRef: {name: agent-sec, key: TOKEN}}
EOF
kubectl apply -f agent.yaml
kubectl -n m5-10 wait --for=condition=Ready pod/agent --timeout=60s
