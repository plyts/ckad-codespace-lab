#!/usr/bin/env bash
# Solution de référence : m3-11 — Ressource personnalisée
kubectl config use-context ckad-a

kubectl api-resources --api-group=ops.m3.lab > ~/ckad/m3-11/resources.txt
kubectl explain maintenance | head -3
cat > obj.yaml <<'EOF'
apiVersion: ops.m3.lab/v1alpha1
kind: Maintenance
metadata: {name: weekly, namespace: m3-11}
spec:
  window: "dimanche 02h"
EOF
kubectl apply -f obj.yaml
