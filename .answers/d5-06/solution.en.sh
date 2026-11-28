#!/usr/bin/env bash
# Reference solution: d5-06 — NetworkPolicy: deny then allow
kubectl config use-context ckad-a
cat > np.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: d5-06
spec:
  podSelector: {}          # all Pods of the namespace
  policyTypes: [Ingress]   # no ingress rule: all incoming traffic is denied
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-frontend
  namespace: d5-06
spec:
  podSelector:
    matchLabels: {app: api}
  policyTypes: [Ingress]
  ingress:
  - from:
    - podSelector:
        matchLabels: {role: frontend}
    ports:
    - protocol: TCP
      port: 80
EOF
kubectl apply -f np.yaml
# Test: kubectl -n d5-06 run f --rm -i --image=busybox:1.37 --restart=Never -l role=frontend -- wget -qO- -T 3 http://api
