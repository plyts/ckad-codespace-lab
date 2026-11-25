#!/usr/bin/env bash
# Solution de référence : m1-01 — Sidecar de journalisation
kubectl config use-context ckad-a

cat > audit.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata: {name: audit, namespace: m1-01}
spec:
  volumes: [{name: shared, emptyDir: {}}]
  initContainers:
  - name: reader
    image: busybox:1.37
    restartPolicy: Always
    command: ["sh", "-c", "tail -F /var/audit/out.log"]
    volumeMounts: [{name: shared, mountPath: /var/audit}]
  containers:
  - name: writer
    image: busybox:1.37
    command: ["sh", "-c", "while true; do echo \"event $(date)\" >> /var/audit/out.log; sleep 2; done"]
    volumeMounts: [{name: shared, mountPath: /var/audit}]
EOF
kubectl apply -f audit.yaml
kubectl -n m1-01 wait --for=condition=Ready pod/audit --timeout=90s
