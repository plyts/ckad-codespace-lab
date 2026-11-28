#!/usr/bin/env bash
# Reference solution: d1-09 — Exam-style: report Pod
kubectl config use-context ckad-a
cat > ~/ckad/d1-09/report.yaml <<'EOF'
apiVersion: v1
kind: Pod
metadata:
  name: report
  namespace: d1-09
spec:
  volumes:
  - name: work
    emptyDir:
      medium: Memory
      sizeLimit: 16Mi
  initContainers:
  - name: stamp
    image: busybox:1.37
    command: ["sh", "-c", "echo 'rapport du jour' > /work/report.txt"]
    volumeMounts:
    - name: work
      mountPath: /work
  containers:
  - name: reader
    image: busybox:1.37
    command: ["sh", "-c", "cat /work/report.txt && sleep 3600"]
    volumeMounts:
    - name: work
      mountPath: /work
EOF
kubectl apply -f ~/ckad/d1-09/report.yaml
kubectl -n d1-09 wait --for=condition=Ready pod/report --timeout=90s
kubectl -n d1-09 logs report -c reader
