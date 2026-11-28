#!/usr/bin/env bash
# Reference solution: d2-09 — Exam-style: Kustomize overlay
kubectl config use-context ckad-a
mkdir -p ~/ckad/d2-09/overlays/prod
cat > ~/ckad/d2-09/overlays/prod/kustomization.yaml <<'EOF'
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
resources:
- ../../base
namespace: d2-09
namePrefix: prod-
labels:
- pairs:
    env: prod
replicas:
- name: web          # name in the base, before the prefix
  count: 3
EOF
kubectl kustomize ~/ckad/d2-09/overlays/prod     # preview
kubectl apply -k ~/ckad/d2-09/overlays/prod
kubectl -n d2-09 rollout status deploy/prod-web --timeout=120s
# VARIANT: commonLabels: {env: prod} also adds the label to selectors (deprecated).
