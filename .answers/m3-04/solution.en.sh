#!/usr/bin/env bash
# Reference solution: m3-04 — Kustomize overlay
kubectl config use-context ckad-a

mkdir -p ~/ckad/m3-04/overlay
cat > ~/ckad/m3-04/overlay/kustomization.yaml <<'EOF'
resources: [../base]
namespace: m3-04
namePrefix: stg-
labels:
- pairs: {tier: staging}
replicas:
- {name: shop, count: 2}
images:
- {name: nginx, newTag: 1.28-alpine}
EOF
kubectl apply -k ~/ckad/m3-04/overlay
kubectl -n m3-04 rollout status deploy/stg-shop --timeout=120s
