#!/usr/bin/env bash
# Reference solution: d4-02 — Secret in a variable
kubectl config use-context ckad-a
kubectl -n d4-02 create secret generic db-cred --from-literal=username=admin --from-literal='password=S3cr3t!'
cat > db-client.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: db-client
  namespace: d4-02
spec:
  containers:
  - name: db-client
    image: busybox:1.37
    command: ["sh", "-c", "sleep 3600"]
    env:
    - name: DB_PASSWORD
      valueFrom:
        secretKeyRef:
          name: db-cred
          key: password
EOF
kubectl apply -f db-client.yaml
kubectl -n d4-02 wait --for=condition=Ready pod/db-client --timeout=60s
