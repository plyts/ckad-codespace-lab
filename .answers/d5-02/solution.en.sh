#!/usr/bin/env bash
# Reference solution: d5-02 — NodePort Service
kubectl config use-context ckad-a
kubectl -n d5-02 expose deploy web --name=web-np --type=NodePort --port=80 --target-port=80 \
  --dry-run=client -o yaml > np.yaml
sed -i 's/  - port: 80/  - nodePort: 30080\n    port: 80/' np.yaml
kubectl apply -f np.yaml
kubectl -n d5-02 get svc web-np
