#!/usr/bin/env bash
# Solution de référence : m4-15 — NetworkPolicy par namespace
kubectl config use-context ckad-a

cat > np.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: from-m4-15-ops, namespace: m4-15}
spec:
  podSelector: {matchLabels: {app: vault}}
  policyTypes: [Ingress]
  ingress:
  - from:
    - namespaceSelector:
        matchLabels: {kubernetes.io/metadata.name: m4-15-ops}
EOF
kubectl apply -f np.yaml
