#!/usr/bin/env bash
# Solution de référence : d4-08 — Utiliser une ressource personnalisée (CRD)
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
kubectl -n d4-08 get backups     # ou : kubectl -n d4-08 get bk
