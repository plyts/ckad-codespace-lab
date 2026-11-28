#!/usr/bin/env bash
# Reference solution: d1-04 — Sidecar following a log file
kubectl config use-context ckad-a
cat > logger.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: logger
  namespace: d1-04
spec:
  volumes:
  - name: logs
    emptyDir: {}
  initContainers:
  - name: shipper                  # sidecar natif : initContainer + restartPolicy Always
    image: busybox:1.37
    restartPolicy: Always
    command: ["sh", "-c", "tail -F /var/log/app/app.log"]
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
  containers:
  - name: app
    image: busybox:1.37
    command: ["sh", "-c", "while true; do echo \"tick $(date)\" >> /var/log/app/app.log; sleep 2; done"]
    volumeMounts:
    - name: logs
      mountPath: /var/log/app
EOF
kubectl apply -f logger.yaml
kubectl -n d1-04 wait --for=condition=Ready pod/logger --timeout=90s
kubectl -n d1-04 logs logger -c shipper --tail=3
# VARIANT (old form): shipper as a second container under containers:.
# It works too, but guarantees neither the start order nor the stop after app.
