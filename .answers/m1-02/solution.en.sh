#!/usr/bin/env bash
# Reference solution: m1-02 — Update with a cause
kubectl config use-context ckad-a

kubectl -n m1-02 set image deploy/storefront nginx=nginx:1.28-alpine
kubectl -n m1-02 annotate deploy storefront kubernetes.io/change-cause='nginx 1.28'
kubectl -n m1-02 scale deploy storefront --replicas=4
kubectl -n m1-02 rollout status deploy/storefront --timeout=120s
