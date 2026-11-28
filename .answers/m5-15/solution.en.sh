#!/usr/bin/env bash
# Reference solution: m5-15 — NetworkPolicy
kubectl config use-context ckad-b

cat > np.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: secrets-api-access, namespace: m5-15}
spec:
  podSelector: {matchLabels: {app: secrets-api}}
  policyTypes: [Ingress]
  ingress:
  - from: [{podSelector: {matchLabels: {access: granted}}}]
    ports: [{protocol: TCP, port: 80}]
EOF
kubectl apply -f np.yaml
