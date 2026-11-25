#!/usr/bin/env bash
# Solution de référence : m4-03 — Sidecar natif
kubectl config use-context ckad-a

cat > trail.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: trail, namespace: m4-03}
spec:
  volumes: [{name: shared, emptyDir: {}}]
  initContainers:
  - name: reader
    image: busybox:1.37
    restartPolicy: Always
    command: ["sh", "-c", "tail -F /trail/out.log"]
    volumeMounts: [{name: shared, mountPath: /trail}]
  containers:
  - name: writer
    image: busybox:1.37
    command: ["sh", "-c", "while true; do echo \"trace $(date)\" >> /trail/out.log; sleep 2; done"]
    volumeMounts: [{name: shared, mountPath: /trail}]
EOF
kubectl apply -f trail.yaml
kubectl -n m4-03 wait --for=condition=Ready pod/trail --timeout=90s
