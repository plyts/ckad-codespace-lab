#!/usr/bin/env bash
# Reference solution: d4-08 — Use a custom resource (CRD)
kubectl config use-context ckad-a
kubectl get crd | grep ckad
kubectl api-resources --api-group=lab.ckad.io
kubectl explain backup.spec
cat > nightly.yaml <<'EOF'
apiVersion: lab.ckad.io/v1
kind: Backup
metadata:
  name: nightly
  namespace: d4-08
spec:
  schedule: "0 2 * * *"
  retention: 7
EOF
kubectl apply -f nightly.yaml
kubectl -n d4-08 get backups     # or: kubectl -n d4-08 get bk
