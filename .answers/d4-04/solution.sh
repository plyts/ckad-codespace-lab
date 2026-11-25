#!/usr/bin/env bash
# Solution de référence : d4-04 — Requests et limits
kubectl config use-context ckad-a
cat > bounded.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: bounded
  namespace: d4-04
spec:
  containers:
  - name: bounded
    image: nginx:1.27-alpine
    resources:
      requests:
        cpu: 100m
        memory: 64Mi
      limits:
        cpu: 200m
        memory: 128Mi
EOF
kubectl apply -f bounded.yaml
kubectl -n d4-04 wait --for=condition=Ready pod/bounded --timeout=60s
kubectl -n d4-04 get pod bounded -o jsonpath='{.status.qosClass}' > ~/ckad/d4-04/qos.txt   # Burstable
