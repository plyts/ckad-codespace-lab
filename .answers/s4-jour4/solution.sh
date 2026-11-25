#!/usr/bin/env bash
# Solution de référence : s4-jour4 — Boutique, journée 4 : isolation réseau et Ingress
kubectl config use-context ckad-a
cat > netpol.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: default-deny, namespace: boutique-j4}
spec:
  podSelector: {}
  policyTypes: [Ingress]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: front-to-api, namespace: boutique-j4}
spec:
  podSelector: {matchLabels: {app: api}}
  policyTypes: [Ingress]
  ingress:
  - from: [{podSelector: {matchLabels: {app: front}}}]
    ports: [{protocol: TCP, port: 5678}]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: api-to-redis, namespace: boutique-j4}
spec:
  podSelector: {matchLabels: {app: redis}}
  policyTypes: [Ingress]
  ingress:
  - from: [{podSelector: {matchLabels: {app: api}}}]
    ports: [{protocol: TCP, port: 6379}]
---
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata: {name: ingress-to-front, namespace: boutique-j4}
spec:
  podSelector: {matchLabels: {app: front}}
  policyTypes: [Ingress]
  ingress:
  - from: [{namespaceSelector: {matchLabels: {kubernetes.io/metadata.name: traefik}}}]
    ports: [{protocol: TCP, port: 80}]
EOF
kubectl apply -f netpol.yaml
kubectl -n boutique-j4 create ingress boutique --class=traefik --rule='boutique.lab.local/*=front:80'
# Depuis le Codespace : curl -H 'Host: boutique.lab.local' http://localhost:8080/
