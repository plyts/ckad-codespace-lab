#!/usr/bin/env bash
# Solution de référence : d4-05 — ResourceQuota et LimitRange
kubectl config use-context ckad-a
kubectl -n d4-05 create quota ns-quota \
  --hard=pods=5,requests.cpu=1,requests.memory=1Gi,limits.cpu=2,limits.memory=2Gi
cat > lr.yaml <<'EOF'
apiVersion: v1
kind: LimitRange
metadata:
  name: defaults
  namespace: d4-05
spec:
  limits:
  - type: Container
    defaultRequest:
      cpu: 50m
      memory: 32Mi
    default:
      cpu: 100m
      memory: 64Mi
EOF
kubectl apply -f lr.yaml
kubectl -n d4-05 run plain --image=nginx:1.27-alpine
kubectl -n d4-05 describe quota ns-quota
