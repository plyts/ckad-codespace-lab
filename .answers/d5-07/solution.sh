#!/usr/bin/env bash
# Solution de référence : d5-07 — NetworkPolicy en sortie (egress)
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
    - namespaceSelector:                     # même élément : namespace ET Pods
        matchLabels:
          kubernetes.io/metadata.name: d5-07-db
      podSelector:
        matchLabels: {app: db}
    ports:
    - {protocol: TCP, port: 80}
  - ports:                                   # DNS vers n'importe quelle destination
    - {protocol: UDP, port: 53}
    - {protocol: TCP, port: 53}
EOF
kubectl apply -f egress.yaml
