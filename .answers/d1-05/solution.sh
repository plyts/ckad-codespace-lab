#!/usr/bin/env bash
# Solution de référence : d1-05 — Init container qui prépare le contenu
kubectl config use-context ckad-a
cat > site.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: site
  namespace: d1-05
  labels:
    app: site
spec:
  volumes:
  - name: html
    emptyDir: {}
  initContainers:
  - name: prepare
    image: busybox:1.37
    command: ["sh", "-c", "echo 'site prêt' > /work/index.html"]
    volumeMounts:
    - name: html
      mountPath: /work
  containers:
  - name: nginx
    image: nginx:1.27-alpine
    ports:
    - containerPort: 80
    volumeMounts:
    - name: html
      mountPath: /usr/share/nginx/html
EOF
kubectl apply -f site.yaml
kubectl -n d1-05 wait --for=condition=Ready pod/site --timeout=90s
