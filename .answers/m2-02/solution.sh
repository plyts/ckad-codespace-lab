#!/usr/bin/env bash
# Solution de référence : m2-02 — Stockage persistant
kubectl config use-context ckad-a

cat > cache-pvc.yaml <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata: {name: cache-pvc, namespace: m2-02}
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: standard
  resources: {requests: {storage: 200Mi}}
---
apiVersion: v1
kind: Pod
metadata: {name: cache, namespace: m2-02}
spec:
  volumes: [{name: data, persistentVolumeClaim: {claimName: cache-pvc}}]
  containers:
  - name: app
    image: busybox:1.37
    command: ["sh", "-c", "echo chaud > /cache/data.txt && sleep 3600"]
    volumeMounts: [{name: data, mountPath: /cache}]
EOF
kubectl apply -f cache-pvc.yaml
kubectl -n m2-02 wait --for=condition=Ready pod/cache --timeout=120s
