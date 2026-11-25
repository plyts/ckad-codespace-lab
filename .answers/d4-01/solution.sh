#!/usr/bin/env bash
# Solution de référence : d4-01 — ConfigMap en variables d'environnement
kubectl config use-context ckad-a
kubectl -n d4-01 create configmap app-config --from-literal=APP_MODE=prod --from-literal=APP_COLOR=blue
cat > app.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: app
  namespace: d4-01
spec:
  containers:
  - name: app
    image: busybox:1.37
    command: ["sh", "-c", "sleep 3600"]
    envFrom:
    - configMapRef:
        name: app-config
EOF
kubectl apply -f app.yaml
kubectl -n d4-01 wait --for=condition=Ready pod/app --timeout=60s
kubectl -n d4-01 exec app -- env | grep APP_
