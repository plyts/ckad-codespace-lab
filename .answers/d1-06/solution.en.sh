#!/usr/bin/env bash
# Reference solution: d1-06 — PersistentVolumeClaim and persistent data
kubectl config use-context ckad-a
cat > pvc.yaml <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: data
  namespace: d1-06
spec:
  accessModes: ["ReadWriteOnce"]
  storageClassName: standard
  resources:
    requests:
      storage: 100Mi
---
apiVersion: v1
kind: Pod
metadata:
  name: writer
  namespace: d1-06
spec:
  volumes:
  - name: data
    persistentVolumeClaim:
      claimName: data
  containers:
  - name: writer
    image: busybox:1.37
    command: ["sh", "-c", "echo persistant > /data/proof.txt && sleep 3600"]
    volumeMounts:
    - name: data
      mountPath: /data
EOF
kubectl apply -f pvc.yaml
kubectl -n d1-06 wait --for=condition=Ready pod/writer --timeout=120s
kubectl -n d1-06 get pvc data
