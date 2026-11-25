#!/usr/bin/env bash
# Solution de référence : d5-09 — Type examen : publier une API protégée
kubectl config use-context ckad-a
kubectl -n d5-09 expose deploy catalog --port=8080 --target-port=5678
kubectl -n d5-09 create ingress catalog --class=traefik --rule='catalog.lab.local/catalog*=catalog:8080'
cat > np.yaml <<'EOF'
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: catalog-from-ingress
  namespace: d5-09
spec:
  podSelector:
    matchLabels: {app: catalog}
  policyTypes: [Ingress]
  ingress:
  - from:
    - namespaceSelector:
        matchLabels:
          kubernetes.io/metadata.name: traefik
    ports:
    - {protocol: TCP, port: 5678}
EOF
kubectl apply -f np.yaml
