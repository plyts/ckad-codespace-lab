#!/usr/bin/env bash
# Reference solution: d5-07 — Egress NetworkPolicy
kubectl config use-context ckad-a
cat > egress.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: client-egress
  namespace: d5-07
spec:
  podSelector:
    matchLabels: {app: client}
  policyTypes: [Egress]
  egress:
  - to:
    - namespaceSelector:                     # same element: namespace AND Pods
        matchLabels:
          kubernetes.io/metadata.name: d5-07-db
      podSelector:
        matchLabels: {app: db}
    ports:
    - {protocol: TCP, port: 80}
  - ports:                                   # DNS to any destination
    - {protocol: UDP, port: 53}
    - {protocol: TCP, port: 53}
EOF
kubectl apply -f egress.yaml
