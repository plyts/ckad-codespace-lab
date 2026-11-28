#!/usr/bin/env bash
# Reference solution: m4-07 — Pending Pod
kubectl config use-context ckad-a

kubectl -n m4-07 describe pod batch | tail -3        # 0/N nodes are available: … didn't match Pod's node affinity/selector
kubectl -n m4-07 get pod batch -o yaml > batch.yaml
yq -i 'del(.spec.nodeSelector)' batch.yaml
kubectl replace --force -f batch.yaml
kubectl -n m4-07 wait --for=condition=Ready pod/batch --timeout=90s
