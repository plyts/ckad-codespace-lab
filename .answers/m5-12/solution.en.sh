#!/usr/bin/env bash
# Reference solution: m5-12 — CRD
kubectl config use-context ckad-b

kubectl api-resources --api-group=data.m5.lab > ~/ckad/m5-12/resources.txt
kubectl explain pipeline | head -3
cat > obj.yaml <<'EOF'
apiVersion: data.m5.lab/v1alpha1
kind: Pipeline
metadata: {name: nightly-etl, namespace: m5-12}
spec:
  source: "s3-bucket"
EOF
kubectl apply -f obj.yaml
