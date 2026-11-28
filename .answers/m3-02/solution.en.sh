#!/usr/bin/env bash
# Reference solution: m3-02 — Init container
kubectl config use-context ckad-b

cat > landing.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: landing, namespace: m3-02}
spec:
  volumes: [{name: html, emptyDir: {}}]
  initContainers:
  - name: seed
    image: busybox:1.37
    command: ["sh", "-c", "echo 'bienvenue m3' > /seed/index.html"]
    volumeMounts: [{name: html, mountPath: /seed}]
  containers:
  - name: web
    image: nginx:1.27-alpine
    volumeMounts: [{name: html, mountPath: /usr/share/nginx/html}]
EOF
kubectl apply -f landing.yaml
kubectl -n m3-02 wait --for=condition=Ready pod/landing --timeout=90s
