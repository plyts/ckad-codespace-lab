#!/usr/bin/env bash
# Reference solution: m5-03 — Init container
kubectl config use-context ckad-a

cat > status.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: status, namespace: m5-03}
spec:
  volumes: [{name: html, emptyDir: {}}]
  initContainers:
  - name: seed
    image: busybox:1.37
    command: ["sh", "-c", "echo 'tout va bien' > /seed/index.html"]
    volumeMounts: [{name: html, mountPath: /seed}]
  containers:
  - name: web
    image: nginx:1.27-alpine
    volumeMounts: [{name: html, mountPath: /usr/share/nginx/html}]
EOF
kubectl apply -f status.yaml
kubectl -n m5-03 wait --for=condition=Ready pod/status --timeout=90s
