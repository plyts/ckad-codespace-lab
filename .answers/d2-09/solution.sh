#!/usr/bin/env bash
# Solution de référence : d2-09 — Type examen : overlay Kustomize
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
- name: web          # nom dans la base, avant le préfixe
  count: 3
EOF
kubectl kustomize ~/ckad/d2-09/overlays/prod     # aperçu
kubectl apply -k ~/ckad/d2-09/overlays/prod
kubectl -n d2-09 rollout status deploy/prod-web --timeout=120s
# VARIANTE : commonLabels: {env: prod} ajoute aussi le label aux sélecteurs (déprécié).
