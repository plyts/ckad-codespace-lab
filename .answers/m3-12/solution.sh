#!/usr/bin/env bash
# Solution de référence : m3-12 — NetworkPolicy d'entrée
kubectl config use-context ckad-a

cat > np.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: ledger-access, namespace: m3-12}
spec:
  podSelector: {matchLabels: {app: ledger}}
  policyTypes: [Ingress]
  ingress:
  - from: [{podSelector: {matchLabels: {role: accounting}}}]
    ports: [{protocol: TCP, port: 80}]
EOF
kubectl apply -f np.yaml
