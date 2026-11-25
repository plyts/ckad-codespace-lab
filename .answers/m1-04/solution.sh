#!/usr/bin/env bash
# Solution de référence : m1-04 — ConfigMap et Secret en variables
kubectl config use-context ckad-a

kubectl -n m1-04 create configmap worker-cfg --from-literal=LEVEL=debug
kubectl -n m1-04 create secret generic worker-sec --from-literal=TOKEN=t0k3n-a1
cat > worker.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: worker, namespace: m1-04}
spec:
  containers:
  - name: app
    image: busybox:1.37
    command: ["sh", "-c", "sleep 3600"]
    env:
    - name: LOG_LEVEL
      valueFrom: {configMapKeyRef: {name: worker-cfg, key: LEVEL}}
    - name: API_TOKEN
      valueFrom: {secretKeyRef: {name: worker-sec, key: TOKEN}}
EOF
kubectl apply -f worker.yaml
kubectl -n m1-04 wait --for=condition=Ready pod/worker --timeout=60s
