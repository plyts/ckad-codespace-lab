#!/usr/bin/env bash
# Solution de référence : m5-02 — PVC
kubectl config use-context ckad-a

cat > media-pvc.yaml <<'EOF'
apiVersion: v1
kind: PersistentVolumeClaim
metadata: {name: media-pvc, namespace: m5-02}
spec:
  accessModes: [ReadWriteOnce]
  storageClassName: standard
  resources: {requests: {storage: 150Mi}}
---
apiVersion: v1
kind: Pod
metadata: {name: media, namespace: m5-02}
spec:
  volumes: [{name: data, persistentVolumeClaim: {claimName: media-pvc}}]
  containers:
  - name: app
    image: busybox:1.37
    command: ["sh", "-c", "echo photo > /media/data.txt && sleep 3600"]
    volumeMounts: [{name: data, mountPath: /media}]
EOF
kubectl apply -f media-pvc.yaml
kubectl -n m5-02 wait --for=condition=Ready pod/media --timeout=120s
