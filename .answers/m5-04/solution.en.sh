#!/usr/bin/env bash
# Reference solution: m5-04 — Kustomize
kubectl config use-context ckad-b

mkdir -p ~/ckad/m5-04/overlay
cat > ~/ckad/m5-04/overlay/kustomization.yaml <<'EOF'
resources: [../base]
namespace: m5-04
namePrefix: prd-
labels:
- pairs: {tier: prod}
replicas:
- {name: shop, count: 3}
images:
- {name: nginx, newTag: 1.28-alpine}
EOF
kubectl apply -k ~/ckad/m5-04/overlay
kubectl -n m5-04 rollout status deploy/prd-shop --timeout=120s
