#!/usr/bin/env bash
# Reference solution: d4-09 — Exam-style: configured application
kubectl config use-context ckad-a
kubectl -n d4-09 create configmap portal-html --from-literal=index.html='Portal OK'
kubectl -n d4-09 create secret generic portal-key --from-literal=API_KEY=k-7731
kubectl -n d4-09 create serviceaccount portal-sa
cat > portal.yaml <<'EOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: portal
  namespace: d4-09
spec:
  replicas: 2
  selector:
    matchLabels: {app: portal}
  template:
    metadata:
      labels: {app: portal}
    spec:
      serviceAccountName: portal-sa
      volumes:
      - name: html
        configMap:
          name: portal-html
      containers:
      - name: nginx
        image: nginx:1.27-alpine
        resources:
          requests: {cpu: 50m, memory: 32Mi}
        env:
        - name: API_KEY
          valueFrom:
            secretKeyRef: {name: portal-key, key: API_KEY}
        volumeMounts:
        - name: html
          mountPath: /usr/share/nginx/html
EOF
kubectl apply -f portal.yaml
kubectl -n d4-09 rollout status deploy/portal --timeout=120s
